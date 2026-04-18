import streamlit as st
from utils.extractor import extract_text_from_pdf
from utils.embedder import get_embedding
from utils.scorer import compute_match_score, generate_feedback
import tempfile
import os

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("📄 AI Resume Analyzer")
st.markdown("Upload your resume and paste a job description to see how well you match.")

# --- INPUT SECTION ---
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste the Job Description here", height=200)

analyze_btn = st.button("Analyze Match")

# --- LOGIC ---
if analyze_btn:
    if not uploaded_file or not job_description.strip():
        st.warning("Please upload a resume AND enter a job description.")
    else:
        # Save uploaded PDF to a temp file (pdfplumber needs a real file path)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text_from_pdf(tmp_path)
            resume_embedding = get_embedding(resume_text)
            jd_embedding = get_embedding(job_description)
            score = compute_match_score(resume_embedding, jd_embedding)
            feedback = generate_feedback(score)

        os.unlink(tmp_path)  # clean up temp file

        # --- OUTPUT SECTION ---
        st.markdown("---")
        st.subheader("Results")
        st.metric(label="Match Score", value=f"{score}%")
        st.info(feedback)