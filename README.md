Travel Order Resolver — bootstrap NER.

- Sujet: extraction d'entités nommées (IOB) sur des données type bottins et corpus Kaggle.
- Fichiers présents: bootstrap.pdf (brief), bottins.csv (annotations inline), corpus.zip (ner.csv, ner_dataset.csv).
- Arborescence: src/ (prétraitement), tests/ (pytest), data/raw et data/processed (gitignore), notebooks/, reports/.
- Dépendances: pandas, numpy, scikit-learn, spaCy, spaCy-transformers, torch, transformers, seqeval, pytest.
- Script: src/preprocess/bottins.py convertit bottins.csv en JSONL (texte, spans, tokens, tags).
- Tests: tests/test_bottins_parser.py couvre le parsing et les tags IOB.
- Environnement: venv Python 3, requirements.txt liste les packages.
