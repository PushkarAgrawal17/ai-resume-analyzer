from utils.extractor import extract_text_from_pdf
from utils.embedder import get_embedding
from utils.scorer import compute_match_score, generate_feedback

# --- INPUTS ---
resume_path = "data/DS Lab - PBL Report.pdf"   # your actual PDF name
job_description = """
We are looking for a software developer with experience in
Python, AIML, data structures, algorithms, leetcode, Matplotlib, Scikit-learn, Tensorflow, Pytorch, MySQL, pandasm, HTML, CSS, javascript and problem solving.
Familiarity with hackathons, project development and teamwork is a plus.
"""

# --- PIPELINE ---
print("Extracting resume text...")
resume_text = extract_text_from_pdf(resume_path)

print("Generating embeddings...")
resume_embedding = get_embedding(resume_text)
jd_embedding = get_embedding(job_description)

print("Computing match score...")
score = compute_match_score(resume_embedding, jd_embedding)
feedback = generate_feedback(score)

# --- OUTPUT ---
print("\n========== RESULTS ==========")
print(f"Match Score : {score}%")
print(f"Feedback    : {feedback}")
print("==============================")