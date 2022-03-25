#!/bin/bash
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download fr_core_news_md