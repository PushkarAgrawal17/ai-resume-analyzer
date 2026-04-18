# 📄 AI Resume Analyzer

A semantic AI-powered web app that analyzes how well your resume matches a job description — giving you a match score, skill gap analysis, section-wise breakdown, and actionable suggestions.

Built with Python, Sentence Transformers, and Streamlit.

---

## 🚀 Features

- **Semantic Match Score** — Compares resume and job description using sentence embeddings and cosine similarity, not just keyword counting
- **Section-wise Score Breakdown** — Scores your Education, Skills, and Projects sections independently against the JD
- **Skill Gap Analysis** — Identifies matched and missing skills using a curated skill database with alias support (e.g. `sklearn` → `scikit-learn`)
- **Actionable Suggestions** — Context-aware feedback based on your match score and missing skills
- **Clean SaaS UI** — Built with Streamlit and custom CSS

---

## 🧠 How It Works
```
Resume (PDF)
│
▼
Extract Text (pdfplumber)
│
├──► Section Splitting ──► Section Scores (per section embedding vs JD)
│
└──► Full Embedding ─────► Overall Cosine Similarity Score
│
Job Description ────────────────────────┘
│
└──► Skill Extraction ──► Matched Skills / Missing Skills / Suggestions
```

1. **Text Extraction** — Resume PDF is parsed using `pdfplumber`
2. **Section Detection** — Resume text is split into Education, Skills, Projects, and General sections using rule-based heading detection
3. **Embedding Generation** — Both resume and JD are converted into 384-dimensional vectors using `all-MiniLM-L6-v2` from Sentence Transformers
4. **Similarity Scoring** — Cosine similarity between vectors gives an overall match percentage
5. **Section Scoring** — Each section is independently embedded and compared to the JD
6. **Skill Matching** — Skills are extracted using a predefined database with alias resolution and word-boundary regex matching

---

## 🏗 Project Structure
```
ai-resume-analyzer/
│
├── app.py                  # Streamlit UI — main entry point
├── main.py                 # CLI runner for quick testing
├── requirements.txt        # Python dependencies
│
├── utils/
│   ├── extractor.py        # PDF text extraction + section splitting
│   ├── embedder.py         # Sentence Transformer model + embedding generation
│   ├── scorer.py           # Cosine similarity + feedback + section scoring
│   └── skills.py           # Skills database, aliases, extraction, comparison
│
└── data/                   # Drop resume PDFs here for CLI testing
```

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| UI | Streamlit |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Similarity | scikit-learn (cosine similarity) |
| PDF Parsing | pdfplumber |
| Skill Matching | Regex + custom skill database |

---

## ⚙️ Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/PushkarAgrawal17/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Create and activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\Activate.ps1

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

> The sentence transformer model (~90MB) will auto-download on first run and cache locally.

---

## 🗺 Roadmap

| Version | Features |
|---|---|
| ✅ V1 | PDF extraction, semantic similarity score |
| ✅ V2 | Skill extraction, gap analysis, suggestions |
| ✅ V3 | Skill aliases, section-wise scoring, UI redesign |