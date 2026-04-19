from utils.extractor import extract_text_from_pdf
from utils.embedder import get_embedding
from utils.scorer import compute_match_score, generate_feedback

# CLI testing only. Main app runs via: python app.py

if __name__ == "__main__":
    resume_path = "data/Pushkar Agrawal - Resume.pdf"
    job_description = """
    We are looking for a Junior Full-Stack AI/ML Engineer.
    Hands-on experience with Python and C++ is required.
    Experience with React, Node.js, FastAPI is essential.
    Familiarity with scikit-learn, tensorflow and pytorch is required.
    Knowledge of MySQL and Git is mandatory.
    """

    print("Extracting resume text...")
    resume_text = extract_text_from_pdf(resume_path)

    print("Generating embeddings...")
    resume_embedding = get_embedding(resume_text)
    jd_embedding = get_embedding(job_description)

    print("Computing match score...")
    score = compute_match_score(resume_embedding, jd_embedding)
    feedback = generate_feedback(score)

    print("\n========== RESULTS ==========")
    print(f"Match Score : {score}%")
    print(f"Feedback    : {feedback}")
    print("==============================")