from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compute_match_score(resume_embedding, jd_embedding):
    """
    Takes two embeddings (numpy arrays).
    Returns a match score as a percentage (0 to 100).
    """
    # reshape needed: cosine_similarity expects 2D arrays
    resume_vec = resume_embedding.reshape(1, -1)
    jd_vec = jd_embedding.reshape(1, -1)

    score = cosine_similarity(resume_vec, jd_vec)[0][0]
    percentage = round(float(score) * 100, 2)

    return percentage


def generate_feedback(score):
    """
    Takes a match score (float).
    Returns a simple human-readable feedback string.
    """
    if score >= 75:
        return "Strong Match ✅ — Your resume aligns well with this job."
    elif score >= 50:
        return "Moderate Match ⚠️ — Consider tailoring your resume more."
    else:
        return "Weak Match ❌ — Significant gaps between resume and job description."


def compute_section_scores(sections, jd_embedding):
    """
    Takes extracted resume sections and JD embedding.
    Returns a dict of section_name -> score percentage.
    """
    from utils.embedder import get_embedding

    section_scores = {}

    for section_name, section_text in sections.items():
        if section_text.strip():  # skip empty sections
            section_embedding = get_embedding(section_text)
            score = compute_match_score(section_embedding, jd_embedding)
            section_scores[section_name] = score
        else:
            section_scores[section_name] = 0.0

    return section_scores


def compute_weighted_score(section_scores):
    """
    Takes section scores dict.
    Returns a single weighted score as a percentage.
    """
    weights = {
        "skills":    0.40,
        "projects":  0.35,
        "education": 0.15,
        "general":   0.10,
    }

    weighted_total = 0.0
    weight_used = 0.0

    for section, weight in weights.items():
        if section in section_scores and section_scores[section] > 0:
            weighted_total += section_scores[section] * weight
            weight_used += weight

    # Normalize in case some sections are missing
    if weight_used == 0:
        return 0.0

    final_score = weighted_total / weight_used
    return round(final_score, 2)