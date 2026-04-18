# AI Resume Analyzer

A semantic resume-job description matcher built with Python.

## Tech Stack
- Sentence Transformers (all-MiniLM-L6-v2)
- scikit-learn (cosine similarity)
- pdfplumber (PDF extraction)
- Streamlit (UI)

## How it works
Converts resume and job description into semantic embeddings
and computes cosine similarity to generate a match score.

## Run locally
pip install -r requirements.txt
streamlit run app.py