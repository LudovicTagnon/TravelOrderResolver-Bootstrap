from __future__ import annotations

import argparse
import csv
import json
import re
from html import unescape
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

TAG_PATTERN = re.compile(r"<(?P<label>[A-Z]+)>(?P<content>.*?)</(?P=label)>", re.DOTALL)
TOKEN_PATTERN = re.compile(r"\w+|[^\w\s]", re.UNICODE)


def parse_annotated_text(raw_text: str) -> Tuple[str, List[Tuple[int, int, str]]]:
    plain_parts: List[str] = []
    entities: List[Tuple[int, int, str]] = []
    cursor = 0
    length = 0

    for match in TAG_PATTERN.finditer(raw_text):
        pre_segment = unescape(raw_text[cursor : match.start()])
        plain_parts.append(pre_segment)
        length += len(pre_segment)

        content = unescape(match.group("content"))
        start = length
        plain_parts.append(content)
        length += len(content)
        end = length

        entities.append((start, end, match.group("label")))
        cursor = match.end()

    tail = unescape(raw_text[cursor:])
    plain_parts.append(tail)

    clean_text = "".join(plain_parts)
    entities.sort(key=lambda e: e[0])
    return clean_text, entities


def tokenize_with_iob(
    text: str, entities: Sequence[Tuple[int, int, str]]
) -> Tuple[List[str], List[str]]:
    tokens: List[str] = []
    tags: List[str] = []
    active_entity_index: int | None = None

    for token_match in TOKEN_PATTERN.finditer(text):
        token = token_match.group()
        start, end = token_match.span()

        entity_index = None
        entity_label = None
        for idx, (ent_start, ent_end, ent_label) in enumerate(entities):
            if start < ent_end and end > ent_start:
                entity_index = idx
                entity_label = ent_label
                break

        if entity_index is None:
            tags.append("O")
            active_entity_index = None
        else:
            prefix = "B" if active_entity_index != entity_index else "I"
            tags.append(f"{prefix}-{entity_label}")
            active_entity_index = entity_index

        tokens.append(token)

    return tokens, tags


def read_bottins_rows(path: Path, limit: int | None = None) -> Iterable[tuple[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        for idx, row in enumerate(reader):
            if not row:
                continue
            text_with_tags = row[0]
            source = row[1] if len(row) > 1 else ""
            yield text_with_tags, source
            if limit is not None and (idx + 1) >= limit:
                break


def convert_file(input_path: Path, output_path: Path, limit: int | None = None) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0

    with output_path.open("w", encoding="utf-8") as out:
        for raw_text, source in read_bottins_rows(input_path, limit=limit):
            clean_text, entities = parse_annotated_text(raw_text)
            tokens, tags = tokenize_with_iob(clean_text, entities)
            record = {
                "text": clean_text,
                "entities": entities,
                "tokens": tokens,
                "tags": tags,
                "source": source,
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1

    return count


def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert Bottins inline-annotated CSV to JSONL with IOB tags."
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to bottins.csv (original inline-tagged data).",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output JSONL path (tokens, tags, text, entities).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional number of rows to process (for quick tests).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print a short progress summary.",
    )
    return parser


def main(argv: List[str] | None = None) -> None:
    parser = build_argparser()
    args = parser.parse_args(argv)

    written = convert_file(args.input, args.output, limit=args.limit)
    if args.verbose:
        print(f"Processed {written} rows from {args.input} -> {args.output}")


if __name__ == "__main__":
    main()
