import streamlit as st
from models.embedding_model import EmbeddingModel
from utils.text_processing import clean_text
from utils.similarity import compute_similarity
from utils.skill_extraction import extract_skills
from utils.job_suggester import suggest_jobs_from_text
from utils.generator import generate_resume_text, generate_cover_letter

try:
    from utils.pdf_utils import extract_text_from_pdf
    PDF_SUPPORT = True
except Exception:
    def extract_text_from_pdf(file_obj):
        return ""

    PDF_SUPPORT = False

try:
    from utils.ai_features import (
        simple_semantic_rewrite, interview_qa_simulator, skill_gap_and_learning_path,
        company_targeted_tailoring, explainable_match_report, resume_pdf_bytes,
        chatbot_response, suggest_roles_and_salary
    )
    AI_SUPPORT = True
except Exception:
    AI_SUPPORT = False

# Load model
model = EmbeddingModel()

st.markdown("""
<style>
body {
    background-color: white !important;
}
.big-header { font-size: 2.8rem; font-weight: 700; color: #2b6cb0; margin-bottom: 0.2rem; }
.small-subtitle { font-size: 1.1rem; color: #2a4365; margin-bottom: 1rem; }
.card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06); }
.highlight { color: #dd6b20; font-weight: 700; }
.quote { color: #2d3748; font-style: italic; padding: 8px 14px; background: #f7fafc; border-radius: 8px; margin-bottom: 10px; }
.logo-row { display: flex; align-items: center; gap: 12px; margin-top: 10px; margin-bottom: 15px; }
.logo-row img { height: 35px; filter: grayscale(40%); opacity: 0.88; }
.sticker { background: #f85149; color: #fff; font-size: 0.9rem; font-weight: 700; display: inline-block; padding: 4px 10px; border-radius: 12px; margin: 6px 4px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-header">🚀 AI Resume Analyzer & Job Match Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="small-subtitle">Pure white UI, powerful tools, and motivational energy to keep you moving forward.</div>', unsafe_allow_html=True)

st.markdown('<div class="logo-row"><img src="https://upload.wikimedia.org/wikipedia/commons/a/ab/Logo_TV_2015.png"/><img src="https://upload.wikimedia.org/wikipedia/commons/0/02/Google_2015_logo.svg"/><img src="https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg"/><img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Stripe_Logo%2C_revised_2016.png"/></div>', unsafe_allow_html=True)

st.markdown('<div class="quote">"Success is not final, failure is not fatal: it is the courage to continue that counts." – Winston Churchill</div>', unsafe_allow_html=True)
st.markdown('<div class="quote">"The only way to do great work is to love what you do." – Steve Jobs</div>', unsafe_allow_html=True)
st.markdown('<div class="quote">"Never, never, never give up." – Winston S. Churchill</div>', unsafe_allow_html=True)

st.markdown('<div class="sticker">NEVER GIVE UP</div><div class="sticker">HUSTLE</div><div class="sticker">LEVEL UP</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔍 Analyze", "✍️ Generate", "🧠 Advanced"])


with tab1:
    st.subheader("Resume Input")
    uploaded_file = st.file_uploader("Upload resume (PDF) or paste text", type=["pdf", "txt"], key="uploader_analyze")
    resume_text_area = st.text_area("Or paste your resume here (required if no upload)", key="resume_text_analyze")
    job_desc = st.text_area("Paste job description here (optional)", key="job_desc_analyze")

    def get_resume_text():
        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf" or uploaded_file.name.lower().endswith(".pdf"):
                return extract_text_from_pdf(uploaded_file)
            else:
                try:
                    return uploaded_file.getvalue().decode("utf-8")
                except Exception:
                    return ""
        return resume_text_area

    if st.button("Analyze"):
        resume_text = get_resume_text()
        if not resume_text:
            st.warning("Please provide a resume (upload or paste).")
        else:
            clean_resume = clean_text(resume_text)
            resume_skills = extract_skills(clean_resume)

            st.subheader("Resume Skills")
            st.write(resume_skills)

            # Suggest jobs based on resume content
            suggested = suggest_jobs_from_text(resume_text)
            if suggested:
                st.subheader("Suggested jobs based on your resume")
                st.write(suggested[:5])

            # If a job description was provided, run the full comparison
            if job_desc and job_desc.strip():
                clean_job = clean_text(job_desc)

                emb_resume = model.encode([clean_resume])[0]
                emb_job = model.encode([clean_job])[0]

                score = compute_similarity(emb_resume, emb_job)

                job_skills = extract_skills(clean_job)
                missing_skills = list(set(job_skills) - set(resume_skills))

                st.subheader("Match Score")
                pct = round(score * 100, 2)
                st.write(f"{pct}%")

                st.markdown("**What this score means:** The score is the cosine similarity between the semantic embeddings of your resume and the job description. It ranges from 0 (no similarity) to 1 (very similar). Higher values indicate the overall meaning and phrasing of your resume more closely match the job description — not just keyword overlap.")

                st.subheader("Missing Skills")
                st.write(missing_skills)

                if missing_skills:
                    st.subheader("Suggestions")
                    st.write("Consider adding these skills if applicable:")
                    st.write(missing_skills)

with tab2:
    st.subheader("Generate Resume & Cover Letter")
    with st.form("gen_form"):
        name = st.text_input("Full name", key="gen_name")
        contact = st.text_input("Contact info (email / phone / LinkedIn)", key="gen_contact")
        education = st.text_area("Education (short)", key="gen_education")
        skills = st.text_area("Skills (comma separated)", key="gen_skills")
        experiences = st.text_area("Experiences (one per line)", key="gen_experiences")
        target_job = st.text_input("Target job title (optional)", key="gen_target_job")
        target_company = st.text_input("Target company (optional)", key="gen_target_company")
        tone = st.selectbox("Tone", ["Professional", "Casual", "Enthusiastic"], key="gen_tone")
        submitted = st.form_submit_button("Generate", key="gen_submit")

    if submitted:
        resume_out = generate_resume_text(name or "", contact or "", education or "", skills or "", experiences or "")
        cover_out = generate_cover_letter(name or "", contact or "", target_job or "", target_company or "", experiences or "", skills or "", tone=tone)

        st.subheader("Generated Resume")
        st.text_area("Resume output", resume_out, height=300)
        st.download_button("Download resume (TXT)", resume_out, file_name="resume.txt")

        st.subheader("Generated Cover Letter")
        st.text_area("Cover letter output", cover_out, height=300)
        st.download_button("Download cover letter (TXT)", cover_out, file_name="cover_letter.txt")

with tab3:
    if not AI_SUPPORT:
        st.warning("Advanced AI features require additional dependencies. Install reportlab and ensure ai_features.py is available.")
    else:
        st.subheader("Advanced AI Features")
        uploaded_file = st.file_uploader("Upload resume (PDF) or paste text", type=["pdf", "txt"], key="uploader_advanced")
        resume_text_area = st.text_area("Or paste your resume here", key="resume_text_advanced")
        job_desc = st.text_area("Job description (for relevant features)", key="job_desc_advanced")
        company = st.text_input("Company name (for tailoring)", key="company_advanced")

        def get_resume_text():
            if uploaded_file is not None:
                if uploaded_file.type == "application/pdf" or uploaded_file.name.lower().endswith(".pdf"):
                    return extract_text_from_pdf(uploaded_file)
                else:
                    try:
                        return uploaded_file.getvalue().decode("utf-8")
                    except Exception:
                        return ""
            return resume_text_area

        feature = st.selectbox("Select Feature", [
            "Semantic Resume Rewriter", "Interview Q&A Simulator", "Skill Gap & Learning Path",
            "Company-Targeted Tailoring", "Explainable Match Report", "Resume Formatting & PDF Export",
            "Interactive Revision Chatbot", "Role Suggestion + Salary Estimate",
            "Q&A Skill Extractor", "Impact Bullet Generator", "Job Title Normalizer", "Email / Follow-up Builder",
            "A/B Resume Comparator"
        ])

        if st.button("Run Feature"):
            resume_text = get_resume_text()
            if not resume_text:
                st.warning("Please provide a resume.")
            else:
                if feature == "Semantic Resume Rewriter":
                    rewritten = simple_semantic_rewrite(resume_text, job_desc.split()[0] if job_desc else None)
                    st.subheader("Rewritten Resume")
                    st.text_area("Output", rewritten, height=400)

                elif feature == "Interview Q&A Simulator":
                    qa_pairs = interview_qa_simulator(resume_text, job_desc)
                    st.subheader("Interview Q&A")
                    for q, a in qa_pairs[:10]:
                        st.write(f"**Q:** {q}")
                        st.write(f"**A:** {a}")
                        st.write("---")

                elif feature == "Skill Gap & Learning Path":
                    if not job_desc:
                        st.warning("Provide job description for skill gap analysis.")
                    else:
                        gap = skill_gap_and_learning_path(resume_text, job_desc)
                        st.subheader("Missing Skills")
                        st.write(gap["missing_skills"])
                        st.subheader("Learning Path")
                        for l in gap["learning_path"]:
                            st.write(f"- {l}")

                elif feature == "Company-Targeted Tailoring":
                    if not company:
                        st.warning("Provide company name.")
                    else:
                        tailored = company_targeted_tailoring(resume_text, company, job_desc)
                        st.subheader("Tailored Resume")
                        st.text_area("Output", tailored["tailored_resume"], height=400)
                        st.subheader("Cover Paragraph")
                        st.write(tailored["cover_paragraph"])

                elif feature == "Explainable Match Report":
                    if not job_desc:
                        st.warning("Provide job description.")
                    else:
                        report = explainable_match_report(model, resume_text, job_desc)
                        st.subheader("Top Matching Sentences")
                        for sent, sim in report[:10]:
                            st.write(f"**{round(sim*100, 2)}%:** {sent}")

                elif feature == "Resume Formatting & PDF Export":
                    pdf_bytes = resume_pdf_bytes(resume_text)
                    if pdf_bytes:
                        st.download_button("Download PDF", pdf_bytes, file_name="resume.pdf", mime="application/pdf")
                    else:
                        st.warning("PDF generation failed. Install reportlab.")

                elif feature == "Interactive Revision Chatbot":
                    user_msg = st.text_input("Chat with the bot (e.g., 'Rewrite my resume')")
                    if user_msg:
                        response = chatbot_response(user_msg, resume_text)
                        st.write(f"**Bot:** {response}")

                elif feature == "Role Suggestion + Salary Estimate":
                    suggestions = suggest_roles_and_salary(resume_text)
                    st.subheader("Suggested Roles & Salaries")
                    for s in suggestions:
                        st.write(f"**{s['role']} ({s['source']}):** ${s['salary_range'][0]:,} - ${s['salary_range'][1]:,}")

                elif feature == "Q&A Skill Extractor":
                    qs = extract_interview_questions(resume_text, job_desc)
                    st.subheader("Generated Interview Questions")
                    for q in qs[:15]:
                        st.write(f"- {q}")

                elif feature == "Impact Bullet Generator":
                    bullets = generate_impact_bullets(resume_text)
                    st.subheader("Impact Bullets")
                    for b in bullets:
                        st.write(f"- {b}")

                elif feature == "Job Title Normalizer":
                    normalized = standardize_job_title(job_desc or "")
                    st.subheader("Standardized Job Title")
                    st.write(normalized)

                elif feature == "Email / Follow-up Builder":
                    candidate = st.text_input("Candidate name", key="followup_name")
                    company_field = st.text_input("Company name", key="followup_company")
                    role_field = st.text_input("Role", key="followup_role")
                    if st.button("Generate Email", key="followup_generate"):
                        template = generate_email_followup(candidate or "Hiring Manager", company_field or "your company", role_field or "the position")
                        st.text_area("Follow-up message", template, height=220)

                elif feature == "A/B Resume Comparator":
                    st.write("This feature compares two resume versions to identify stronger semantic match components.")
                    version_a = st.text_area("Resume version A", key="ab_a")
                    version_b = st.text_area("Resume version B", key="ab_b")
                    if st.button("Compare versions", key="ab_compare"):
                        if not version_a or not version_b:
                            st.warning("Please enter both versions")
                        else:
                            sa = model.encode([clean_text(version_a)])[0]
                            sb = model.encode([clean_text(version_b)])[0]
                            sj = model.encode([clean_text(job_desc or "")])[0] if job_desc else None
                            sim_a = compute_similarity(sa, sj) if sj is not None else None
                            sim_b = compute_similarity(sb, sj) if sj is not None else None
                            st.write(f"Version A similarity: {round(sim_a * 100,2) if sim_a is not None else 'N/A'}%")
                            st.write(f"Version B similarity: {round(sim_b * 100,2) if sim_b is not None else 'N/A'}%")
                            if sim_a is not None and sim_b is not None:
                                winner = 'A' if sim_a > sim_b else 'B' if sim_b > sim_a else 'Tie'
                                st.write(f"Better fit: {winner}")
