from utils.extractor import extract_text_from_pdf
from utils.embedder import get_embedding, model
from utils.scorer import compute_match_score, generate_feedback
from utils.explainer import split_into_sentences, get_top_matches
from utils.skills import extract_skills_fuzzy

# This file is for quick CLI testing only.
# The main app runs via: streamlit run app.py

if __name__ == "__main__":
    resume_path = "data/Pushkar Agrawal - Resume.pdf"
    job_description = """
    We are looking for a Junior AI/ML Engineer with hands-on experience
    in Python and machine learning, scikit-learn, tensorflow, pytorch.
    Familiarity with docker, aws and nlp is a plus.
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


    text = extract_text_from_pdf("data/Pushkar Agrawal - Resume.pdf")
    sentences = split_into_sentences(text)

    print(f"Total sentences extracted: {len(sentences)}")
    for i, s in enumerate(sentences):
        print(f"{i+1}. {s}")


resume_text = extract_text_from_pdf("data/Pushkar Agrawal - Resume.pdf")
jd_text = """We are looking for a Junior Software Engineer with strong problem solving abilities and hands-on experience in Python and C++.
Experience building full-stack applications using React, Node.js, and FastAPI.
Familiarity with scikit-learn, tensorflow and machine learning is required.
Knowledge of Git and MySQL is mandatory.
Experience with Docker and AWS is a plus.
Strong teamwork and communication skills are valued.
"""

matches = get_top_matches(resume_text, jd_text, model, top_n=5)

print("\n===== TOP MATCHING PAIRS =====")
for i, (r, j, score) in enumerate(matches):
    print(f"\nMatch {i+1} — Score: {score}%")
    print(f"  Resume : {r[:100]}")
    print(f"  JD     : {j[:100]}")


test_text = "I have experience with machine-learning, pytorch and sklearn"
print(extract_skills_fuzzy(test_text))

test_text = "I have experience with java and javascript"
print(extract_skills_fuzzy(test_text))


test1 = "I have experience with java and javascript"
test2 = "I have experience with javascript only"

print("Test 1:", extract_skills_fuzzy(test1))
print("Test 2:", extract_skills_fuzzy(test2))