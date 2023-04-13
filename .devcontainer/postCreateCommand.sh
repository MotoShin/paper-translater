#!/bin/bash
pip install --upgrade pip
pip install --user -r requirements.txt
python -c "import nltk; nltk.download('punkt')"
