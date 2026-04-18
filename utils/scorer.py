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