import re
from rapidfuzz import fuzz

SKILLS_DB = {
    "languages": [
        "python", "c++", "java", "javascript", "typescript",
        "sql", "html", "css", "r", "go"
    ],
    "ai_ml": [
        "machine learning", "deep learning", "nlp", "computer vision",
        "supervised learning", "unsupervised learning", "classification",
        "regression", "clustering", "model evaluation", "overfitting",
        "neural networks", "reinforcement learning", "feature engineering"
    ],
    "libraries": [
        "numpy", "pandas", "matplotlib", "scikit-learn", "tensorflow",
        "pytorch", "keras", "opencv", "huggingface", "streamlit",
        "fastapi", "flask", "react", "nodejs"
    ],
    "tools": [
        "git", "docker", "mysql", "mongodb", "postgresql",
        "linux", "aws", "gcp", "azure", "kubernetes",
        "postman", "vs code", "jupyter"
    ],
    "soft_skills": [
        "teamwork", "adaptability", "problem solving", "communication",
        "leadership", "time management"
    ]
}

SKILL_ALIASES = {
    "sql":          ["mysql", "postgresql", "sqlite"],
    "javascript":   ["js", "node.js", "nodejs"],
    "scikit-learn": ["sklearn"],
    "tensorflow":   ["tf"],
    "c++":          ["cpp"],
    "nlp":          ["natural language processing"],
    "computer vision": ["cv", "opencv"],
    "aws":          ["amazon web services"],
    "gcp":          ["google cloud"],
}

EXACT_MATCH_ONLY = {
    "java", "r", "go", "c", "rust", "scala"
}


def extract_skills(text):
    text_lower = text.lower()
    found_skills = set()

    # Step 1: direct matching (same as before)
    for category, skill_list in SKILLS_DB.items():
        for skill in skill_list:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)

    # Step 2: alias matching
    for canonical_skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = r'\b' + re.escape(alias) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(canonical_skill)  # credit the canonical skill

    return found_skills


def extract_skills_fuzzy(text, threshold=80):
    """
    Extends extract_skills with fuzzy matching.
    Catches skill variants like 'machine-learning', 'pytorch3', etc.
    threshold: 0-100, higher = stricter matching
    """
    # Start with exact + alias matches
    found_skills = extract_skills(text)

    text_lower = text.lower()
    words = text_lower.split()

    # Build n-grams (1, 2, 3 word combinations) to match multi-word skills
    ngrams = []
    for n in range(1, 4):
        for i in range(len(words) - n + 1):
            ngram = " ".join(words[i:i+n])
            ngrams.append(ngram)

    # Fuzzy match each ngram against every skill in DB
    for canonical_skill, skill_list in SKILLS_DB.items():
        for skill in skill_list:
            if skill in found_skills:
                continue

            # Skip fuzzy for skills that need exact matching
            if skill in EXACT_MATCH_ONLY:
                continue

            for ngram in ngrams:
                score = fuzz.ratio(ngram, skill)
                if score >= threshold:
                    found_skills.add(skill)
                    break

    return found_skills


def compare_skills(resume_text, jd_text):
    """
    Compares skills between resume and job description.
    Returns matched skills, missing skills.
    """

    resume_skills = extract_skills_fuzzy(resume_text)
    jd_skills = extract_skills_fuzzy(jd_text)


    matched = resume_skills & jd_skills   # intersection
    missing = jd_skills - resume_skills   # in JD but not in resume

    return matched, missing, jd_skills  