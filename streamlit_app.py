import streamlit as st
from utils.skills import compare_skills
from utils.embedder import get_embedding, model
from utils.extractor import extract_text_from_pdf, extract_sections
from utils.scorer import compute_match_score, generate_feedback, compute_section_scores, compute_weighted_score
from utils.explainer import get_top_matches
import tempfile
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Deep navy background with glow */
    .stApp {
        background: radial-gradient(ellipse at 20% 20%, #0f1a3d 0%, #080d1f 50%, #0a0f2e 100%);
        min-height: 100vh;
    }

    /* Glowing orbs in background */
    .stApp::before {
        content: '';
        position: fixed;
        top: -20%;
        left: -10%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.12) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }

    .stApp::after {
        content: '';
        position: fixed;
        bottom: -20%;
        right: -10%;
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.10) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }

    /* Hero title */
    .hero-wrapper {
        text-align: center;
        padding: 3rem 0 2rem 0;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.4);
        color: #a78bfa;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 0.35rem 1rem;
        border-radius: 999px;
        margin-bottom: 1.2rem;
    }

    .hero-title {
        font-size: 3.2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #e0e7ff 0%, #a78bfa 50%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.15;
        margin-bottom: 1rem;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #64748b;
        max-width: 520px;
        margin: 0 auto 2.5rem auto;
        line-height: 1.6;
    }

    /* Input card */
    .input-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 0 40px rgba(99, 102, 241, 0.08), 0 20px 60px rgba(0,0,0,0.4);
        margin-bottom: 1.5rem;
    }

    .input-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }

    /* Streamlit file uploader override */
    [data-testid="stFileUploader"] {
        background: rgba(99, 102, 241, 0.05);
        border: 1.5px dashed rgba(99, 102, 241, 0.35);
        border-radius: 12px;
        padding: 0.5rem;
        transition: border-color 0.2s;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: rgba(139, 92, 246, 0.6);
    }

    /* Textarea override */
    [data-testid="stTextArea"] textarea {
        background: rgba(99, 102, 241, 0.05) !important;
        border: 1.5px solid rgba(99, 102, 241, 0.25) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-size: 0.9rem !important;
        resize: none;
    }

    [data-testid="stTextArea"] textarea:focus {
        border-color: rgba(139, 92, 246, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }

    /* Analyze button */
    [data-testid="stButton"] > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.75rem 2rem !important;
        width: 100% !important;
        letter-spacing: 0.03em !important;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.35) !important;
        transition: all 0.2s !important;
    }

    [data-testid="stButton"] > button:hover {
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.55) !important;
        transform: translateY(-1px) !important;
    }

    /* Score card */
    .score-card {
        background: linear-gradient(135deg, #1e1b4b, #312e81);
        border: 1px solid #4338ca;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 0 40px rgba(99, 102, 241, 0.2);
    }

    .score-number {
        font-size: 4rem;
        font-weight: 900;
        color: #a78bfa;
        line-height: 1;
    }

    .score-label {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 0.4rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }

    /* Section score cards */
    .section-card {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }

    .section-score {
        font-size: 1.8rem;
        font-weight: 700;
        color: #e2e8f0;
    }

    .section-name {
        font-size: 0.75rem;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.2rem;
    }

    /* Skill chips */
    .chip-matched {
        display: inline-block;
        background: #052e16;
        color: #4ade80;
        border: 1px solid #166534;
        border-radius: 999px;
        padding: 0.3rem 0.9rem;
        font-size: 0.85rem;
        margin: 0.25rem;
        font-weight: 500;
    }

    .chip-missing {
        display: inline-block;
        background: #2d0a0a;
        color: #f87171;
        border: 1px solid #7f1d1d;
        border-radius: 999px;
        padding: 0.3rem 0.9rem;
        font-size: 0.85rem;
        margin: 0.25rem;
        font-weight: 500;
    }

    .section-heading {
        font-size: 0.82rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin: 2rem 0 1rem 0;
    }

    .suggestion-box {
        background: rgba(28, 25, 23, 0.8);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        color: #fcd34d;
        font-size: 0.95rem;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- HERO ---
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-badge">⚡ Semantic AI Matching</div>
    <div class="hero-title">AI Resume Analyzer</div>
    <div class="hero-subtitle">
        Paste a job description and upload your resume — get an instant
        match score, skill gap analysis, and actionable suggestions.
    </div>
</div>
""", unsafe_allow_html=True)

# --- INPUT CARD ---

col_upload, col_jd = st.columns([1, 1])

with col_upload:
    st.markdown('<div class="input-label">📎 Resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

with col_jd:
    st.markdown('<div class="input-label">📋 Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area("", height=160,
        placeholder="Paste the job description here...",
        label_visibility="collapsed")


analyze_btn = st.button("⚡ Analyze Match", use_container_width=True)

# --- LOGIC ---
if analyze_btn:
    if not uploaded_file or not job_description.strip():
        st.warning("⚠️ Please upload a resume AND enter a job description.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text_from_pdf(tmp_path)
            sections = extract_sections(resume_text)
            resume_embedding = get_embedding(resume_text)
            jd_embedding = get_embedding(job_description)
            score = compute_match_score(resume_embedding, jd_embedding)
            feedback = generate_feedback(score)
            matched_skills, missing_skills, jd_skills = compare_skills(resume_text, job_description)
            section_scores = compute_section_scores(sections, jd_embedding)
            weighted_score = compute_weighted_score(section_scores, matched_skills, jd_skills)
            top_matches = get_top_matches(resume_text, job_description, model, top_n=5)

        os.unlink(tmp_path)

        # --- OVERALL SCORE ---
        st.markdown("---")
        st.markdown(f"""
        <div class="score-card">
            <div class="score-number">{weighted_score}%</div>
            <div class="score-label">Overall Match Score</div>
        </div>
        """, unsafe_allow_html=True)

        # --- FEEDBACK BANNER ---
        st.info(feedback)

        # --- SECTION SCORES ---
        st.markdown('<div class="section-heading">📊 Score by Section</div>', unsafe_allow_html=True)
        sec_cols = st.columns(len(section_scores))
        for col, (section, sec_score) in zip(sec_cols, section_scores.items()):
            with col:
                st.markdown(f"""
                <div class="section-card">
                    <div class="section-score">{sec_score}%</div>
                    <div class="section-name">{section.capitalize()}</div>
                </div>
                """, unsafe_allow_html=True)

        # --- SKILLS ---
        st.markdown('<div class="section-heading">🧠 Skill Analysis</div>', unsafe_allow_html=True)
        sk_col1, sk_col2 = st.columns(2)

        with sk_col1:
            st.markdown("**✅ Matched Skills**")
            if matched_skills:
                chips = "".join([f'<span class="chip-matched">{s}</span>' for s in sorted(matched_skills)])
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.caption("No matching skills found.")

        with sk_col2:
            st.markdown("**❌ Missing Skills**")
            if missing_skills:
                chips = "".join([f'<span class="chip-missing">{s}</span>' for s in sorted(missing_skills)])
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.caption("No missing skills — great match!")

        # --- SUGGESTION ---
        if missing_skills:
            st.markdown('<div class="section-heading">💡 Suggestions</div>', unsafe_allow_html=True)
            suggestions = []

            # Skill-based suggestion
            if missing_skills:
                suggestions.append(f"<strong>🛠 Skills Gap:</strong> Consider adding these missing skills to your resume: <strong>{', '.join(sorted(missing_skills))}</strong>.")

            # Section-based suggestions
            if section_scores.get("skills", 100) < 50:
                suggestions.append("<strong>📝 Skills Section:</strong> Your skills section has low alignment. Try mirroring the exact keywords from the job description.")

            if section_scores.get("projects", 100) < 40:
                suggestions.append("<strong>🚀 Projects Section:</strong> Rewrite your project descriptions to include more keywords from the job description — focus on technologies and outcomes.")

            if section_scores.get("education", 100) < 35:
                suggestions.append("<strong>🎓 Education Section:</strong> Highlight relevant courses or academic projects that align with this role.")

            if not suggestions:
                st.markdown("""
                <div class="suggestion-box">
                    ✅ Your resume is well aligned with this job description. Keep it up!
                </div>
                """, unsafe_allow_html=True)
            else:
                for suggestion in suggestions:
                    st.markdown(f"""
                    <div class="suggestion-box" style="margin-bottom: 0.75rem;">
                        {suggestion}
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown('<div class="section-heading">🔍 Why This Score — Top Matching Lines</div>', unsafe_allow_html=True)

        for i, (r_sent, jd_sent, score) in enumerate(top_matches):
            st.markdown(f"""
            <div style="
                background: rgba(15,23,42,0.8);
                border: 1px solid rgba(99,102,241,0.2);
                border-radius: 12px;
                padding: 1rem 1.25rem;
                margin-bottom: 0.75rem;
            ">
                <div style="color:#64748b; font-size:0.75rem; margin-bottom:0.5rem;">
                    MATCH {i+1} &nbsp;·&nbsp;
                    <span style="color:#a78bfa; font-weight:700;">{score}%</span>
                </div>
                <div style="color:#e2e8f0; font-size:0.88rem; margin-bottom:0.4rem;">
                    📄 <strong>Resume:</strong> {r_sent[:120]}...
                </div>
                <div style="color:#94a3b8; font-size:0.85rem;">
                    💼 <strong>JD:</strong> {jd_sent[:120]}...
                </div>
            </div>
            """, unsafe_allow_html=True)