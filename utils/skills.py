import re

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


def compare_skills(resume_text, jd_text):
    """
    Compares skills between resume and job description.
    Returns matched skills, missing skills.
    """
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = resume_skills & jd_skills   # intersection
    missing = jd_skills - resume_skills   # in JD but not in resume

    return matched, missing