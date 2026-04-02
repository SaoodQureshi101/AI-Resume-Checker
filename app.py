import streamlit as st
from models.embedding_model import EmbeddingModel
from utils.text_processing import clean_text
from utils.similarity import compute_similarity
from utils.skill_extraction import extract_skills
try:
    from utils.pdf_utils import extract_text_from_pdf
    PDF_SUPPORT = True
except Exception:
    # PyPDF2 not installed or import failed — disable PDF support gracefully
    def extract_text_from_pdf(file_obj):
        return ""

    PDF_SUPPORT = False
from utils.job_suggester import suggest_jobs_from_text

# Load model
model = EmbeddingModel()

st.title("AI Resume Analyzer & Job Match Assistant")

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
                from utils.pdf_utils import extract_text_from_pdf

if st.button("Analyze"):
    resume_text = get_resume_text()
    if not resume_text:
        st.warning("Please provide a resume (upload or paste).")
    else:
        clean_resume = clean_text(resume_text)
        resume_skills = extract_skills(clean_resume)

        st.subheader("Resume Skills")
        st.write(resume_skills)

            st.title("AI Resume Analyzer & Job Match Assistant")

            mode = st.selectbox("Mode", ["Analyze", "Generate"], index=0)

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
    
            else:  # Generate mode
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