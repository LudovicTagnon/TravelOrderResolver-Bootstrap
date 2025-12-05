# Travel Order Resolver — NER Bootstrap

Starter scaffold to explore Named Entity Recognition for travel-order style data. The repository ships with the assignment spec (`bootstrap.pdf`), the Kaggle corpus (`corpus.zip` containing `ner_dataset.csv` and `ner.csv`), and the annotated `bottins.csv` directory entries.

## Repository Layout
- `bootstrap.pdf`: assignment brief.
- `corpus.zip`: warm-up NER datasets; keep under `data/raw/` when unzipped.
- `bottins.csv`: French annotated entries with inline tags.
- `src/`: Python package for data prep; see `src/preprocess/bottins.py`.
- `data/raw/`, `data/processed/`: input/output data roots (gitignored).
- `notebooks/`, `reports/`, `tests/`: experiments, artifacts, tests.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Data Pointers
- Place large inputs in `data/raw/` (e.g., `corpus.zip`, `bottins.csv`). The originals currently live at the repo root; move or symlink them if convenient.
- Avoid committing extracted corpora or model artifacts; regenerate from scripts/notebooks.

## Preprocess Bottins (inline tags → tokens/IOB)
Convert the annotated directory lines into plain text, entity spans, and IOB tags:
```bash
python -m src.preprocess.bottins --input bottins.csv \
  --output data/processed/bottins.jsonl
```
Options: `--limit N` to sample rows, `--verbose` for progress. Output is JSONL with `text`, `entities` (offsets), `tokens`, `tags`, and `source`.

## Warm-up with Kaggle Corpus
- Unzip the corpus when needed: `unzip corpus.zip -d data/raw`.
- `ner_dataset.csv` is token+tag per line; `ner.csv` includes engineered features. Start with a spaCy baseline, then compare to a Transformer model (e.g., CamemBERT).

## Testing & Quality
- Add unit tests under `tests/` (pytest). Keep fixtures small and deterministic.
- Run optional lint/format if installed: `ruff src tests` and `black src tests`.

## Next Steps
- Build baseline training/eval pipelines for both datasets.
- Track metrics per entity type; log runs under `reports/`.
- Document any new commands in `AGENTS.md` as the workflow solidifies.
