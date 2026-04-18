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

import re

def extract_skills(text):
    """
    Takes any text (resume or JD).
    Returns a set of matched skills from SKILLS_DB.
    """
    text_lower = text.lower()
    found_skills = set()

    for category, skill_list in SKILLS_DB.items():
        for skill in skill_list:
            # Use word boundary matching for short/ambiguous skills
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)

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