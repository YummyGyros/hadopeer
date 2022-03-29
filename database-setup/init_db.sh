#!/bin/bash
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download fr_core_news_md
# FAUNADB_SECRET=your_secret python3 main.py
deactivate