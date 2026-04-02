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

st.title("AI Resume Analyzer & Job Match Assistant")

mode = st.selectbox("Mode", ["Analyze", "Generate", "Advanced"], index=0)

if mode == "Analyze":
    st.subheader("Resume Input")
    uploaded_file = st.file_uploader("Upload resume (PDF) or paste text", type=["pdf", "txt"])
    resume_text_area = st.text_area("Or paste your resume here (required if no upload)")
    job_desc = st.text_area("Paste job description here (optional)")

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

elif mode == "Generate":
    st.subheader("Generate Resume & Cover Letter")
    with st.form("gen_form"):
        name = st.text_input("Full name")
        contact = st.text_input("Contact info (email / phone / LinkedIn)")
        education = st.text_area("Education (short)")
        skills = st.text_area("Skills (comma separated)")
        experiences = st.text_area("Experiences (one per line)")
        target_job = st.text_input("Target job title (optional)")
        target_company = st.text_input("Target company (optional)")
        tone = st.selectbox("Tone", ["Professional", "Casual", "Enthusiastic"])
        submitted = st.form_submit_button("Generate")

    if submitted:
        resume_out = generate_resume_text(name or "", contact or "", education or "", skills or "", experiences or "")
        cover_out = generate_cover_letter(name or "", contact or "", target_job or "", target_company or "", experiences or "", skills or "", tone=tone)

        st.subheader("Generated Resume")
        st.text_area("Resume output", resume_out, height=300)
        st.download_button("Download resume (TXT)", resume_out, file_name="resume.txt")

        st.subheader("Generated Cover Letter")
        st.text_area("Cover letter output", cover_out, height=300)
        st.download_button("Download cover letter (TXT)", cover_out, file_name="cover_letter.txt")

elif mode == "Advanced":
    if not AI_SUPPORT:
        st.warning("Advanced AI features require additional dependencies. Install reportlab and ensure ai_features.py is available.")
    else:
        st.subheader("Advanced AI Features")
        uploaded_file = st.file_uploader("Upload resume (PDF) or paste text", type=["pdf", "txt"])
        resume_text_area = st.text_area("Or paste your resume here")
        job_desc = st.text_area("Job description (for relevant features)")
        company = st.text_input("Company name (for tailoring)")

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
            "Interactive Revision Chatbot", "Role Suggestion + Salary Estimate"
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
                        st.write(f"**{s['role']}:** ${s['salary_range'][0]:,} - ${s['salary_range'][1]:,}")