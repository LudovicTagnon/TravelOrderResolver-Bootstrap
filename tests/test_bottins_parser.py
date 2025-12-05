from src.preprocess.bottins import parse_annotated_text, tokenize_with_iob


def test_parse_and_tokenize_basic():
    raw = "<PER>Jean Dupont</PER> à <LOC>Paris</LOC>."
    text, entities = parse_annotated_text(raw)
    assert text == "Jean Dupont à Paris."
    assert entities == [(0, 11, "PER"), (14, 19, "LOC")]

    tokens, tags = tokenize_with_iob(text, entities)
    assert tokens == ["Jean", "Dupont", "à", "Paris", "."]
    assert tags == ["B-PER", "I-PER", "O", "B-LOC", "O"]


def test_unescapes_html_entities():
    raw = "Rue d&apos;Anjou <CARDINAL>5</CARDINAL>"
    text, entities = parse_annotated_text(raw)
    assert text == "Rue d'Anjou 5"
    assert entities == [(12, 13, "CARDINAL")]
