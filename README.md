# AI Resume Analyzer

A semantic AI-powered web application that analyzes how well your resume matches a job description.
Upload a PDF resume, paste a job description, and get an instant match score, skill gap analysis,
section-wise breakdown, and actionable suggestions — powered by sentence embeddings and cosine similarity.

---

## Features

**Semantic Match Score**
Compares resume and job description using sentence embeddings and cosine similarity — not keyword counting.
Understands meaning, not just word overlap.

**Explainability — Why This Score**
Shows the top 5 matching sentence pairs between your resume and the JD, so you know exactly why
you got the score you did.

**Section-wise Score Breakdown**
Scores your Education, Skills, and Projects sections independently against the JD,
with configurable weights (Skills 50%, Projects 30%, Education 15%, General 5%).

**Skill Gap Analysis**
Identifies matched and missing skills using a curated skill database with alias support
(e.g. `sklearn` -> `scikit-learn`, `nodejs` -> `javascript`) and fuzzy matching for variants
like `machine-learning` -> `machine learning`.

**Actionable Suggestions**
Context-aware feedback based on your match score, missing skills, and section performance.

---

## How It Works

```
Resume (PDF)
     |
     v
Extract Text (pdfplumber)
     |
     |---> Section Splitting ---> Section Scores (per section embedding vs JD)
     |
     +---> Full Embedding ------> Weighted Cosine Similarity Score
                                          |
Job Description --------------------------+
     |
     +---> Skill Extraction ---> Matched Skills / Missing Skills / Suggestions
                                          |
     +---> Sentence Splitting ---> Top Matching Pairs (Explainability)
```

1. **Text Extraction** — Resume PDF is parsed page by page using `pdfplumber`
2. **Section Detection** — Resume text is split into Education, Skills, Projects, and General using rule-based heading detection
3. **Embedding Generation** — Both resume and JD are converted into 384-dimensional vectors using `all-MiniLM-L6-v2`
4. **Weighted Scoring** — Section scores are combined using configurable weights for a final match percentage
5. **Skill Matching** — Skills extracted via keyword database, alias resolution, regex word-boundary matching, and fuzzy matching
6. **Explainability** — Sentence-level embeddings compared across resume and JD to surface the top matching pairs

---

## Project Structure

```
ai-resume-analyzer/
|
+-- app.py                  # Flask application — routes and pipeline
+-- main.py                 # CLI runner for quick testing
+-- requirements.txt        # Python dependencies
|
+-- utils/
|   +-- extractor.py        # PDF text extraction + section splitting
|   +-- embedder.py         # Sentence Transformer model + embedding generation
|   +-- scorer.py           # Cosine similarity, weighted scoring, feedback
|   +-- skills.py           # Skills database, aliases, fuzzy extraction, comparison
|   +-- explainer.py        # Sentence splitting + top match pair extraction
|
+-- templates/
|   +-- index.html          # Main UI template
|
+-- static/
|   +-- style.css           # Custom CSS — dark navy SaaS design
|
+-- data/                   # Drop resume PDFs here for CLI testing
```

---

## Tech Stack

| Layer            | Technology                                      |
|------------------|-------------------------------------------------|
| Language         | Python 3.10+                                    |
| Web Framework    | Flask                                           |
| UI               | HTML + CSS (custom dark SaaS design)            |
| Embeddings       | Sentence Transformers (`all-MiniLM-L6-v2`)      |
| Similarity       | scikit-learn (cosine similarity)                |
| PDF Parsing      | pdfplumber                                      |
| Skill Matching   | Regex + rapidfuzz + custom skill database       |

---

## Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/PushkarAgrawal17/ai-resume-analyzer.git
cd ai-resume-analyzer
```

**2. Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\Activate.ps1

# Mac / Linux
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

> The sentence transformer model (~90MB) will auto-download on first run and cache locally.

---

## Roadmap

| Version | Status | Features                                              |
|---------|--------|-------------------------------------------------------|
| V1      | Done   | PDF extraction, semantic similarity score             |
| V2      | Done   | Skill extraction, gap analysis, suggestions           |
| V3      | Done   | Skill aliases, section-wise scoring, UI redesign      |
| V4      | Done   | Explainability, weighted scoring, fuzzy skill matching, Flask migration |

---

## Screenshots

> Coming soon

---

## Author

**Pushkar Agrawal**
B.Tech CSE — Jaypee Institute of Information Technology, Noida (2024–2028)

[GitHub](https://github.com/PushkarAgrawal17) · [LinkedIn](https://linkedin.com/in/pushkaragrawal17) · [LeetCode](https://leetcode.com/u/pushkar17)