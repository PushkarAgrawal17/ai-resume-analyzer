import os
import tempfile
from flask import Flask, render_template, request
from utils.extractor import extract_text_from_pdf, extract_sections
from utils.embedder import get_embedding, model
from utils.scorer import compute_match_score, generate_feedback, compute_section_scores, compute_weighted_score
from utils.skills import compare_skills
from utils.explainer import get_top_matches

app = Flask(__name__)

# ---- Route: Home Page ----
@app.route("/")
def index():
    return render_template("index.html")


# ---- Route: Analyze ----
@app.route("/analyze", methods=["POST"])
def analyze():
    resume_file = request.files.get("resume")
    job_description = request.form.get("job_description", "").strip()

    # Basic validation
    if not resume_file or not job_description:
        return render_template("index.html", error="Please upload a resume AND enter a job description.")

    # Save PDF to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        resume_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        # --- Run the full pipeline ---
        resume_text = extract_text_from_pdf(tmp_path)
        sections = extract_sections(resume_text)

        resume_embedding = get_embedding(resume_text)
        jd_embedding = get_embedding(job_description)

        score = compute_match_score(resume_embedding, jd_embedding)
        section_scores = compute_section_scores(sections, jd_embedding)
        matched_skills, missing_skills, jd_skills = compare_skills(resume_text, job_description)
        weighted_score = compute_weighted_score(section_scores, matched_skills, jd_skills)
        feedback = generate_feedback(weighted_score)
        top_matches = get_top_matches(resume_text, job_description, model, top_n=5)

        # --- Build suggestions ---
        suggestions = []
        if missing_skills:
            suggestions.append(f"🛠 <strong>Skills Gap:</strong> Consider adding: <strong>{', '.join(sorted(missing_skills))}</strong>.")
        if section_scores.get("skills", 100) < 50:
            suggestions.append("📝 <strong>Skills Section:</strong> Try mirroring exact keywords from the job description.")
        if section_scores.get("projects", 100) < 40:
            suggestions.append("🚀 <strong>Projects Section:</strong> Rewrite descriptions to include more JD keywords.")
        if section_scores.get("education", 100) < 35:
            suggestions.append("🎓 <strong>Education Section:</strong> Highlight relevant courses that align with this role.")

    finally:
        os.unlink(tmp_path)  # always clean up

    return render_template("index.html",
        weighted_score=weighted_score,
        feedback=feedback,
        section_scores=section_scores,
        matched_skills=sorted(matched_skills),
        missing_skills=sorted(missing_skills),
        suggestions=suggestions,
        top_matches=top_matches,
        filename=resume_file.filename,
    )


if __name__ == "__main__":
    app.run(debug=True)