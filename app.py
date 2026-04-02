import streamlit as st
from models.embedding_model import EmbeddingModel
from utils.text_processing import clean_text
from utils.similarity import compute_similarity
from utils.skill_extraction import extract_skills

# Load model
model = EmbeddingModel()

st.title("AI Resume Analyzer & Job Match Assistant")

resume_text = st.text_area("Paste your resume here")
job_desc = st.text_area("Paste job description here")

if st.button("Analyze"):
    if resume_text and job_desc:
        clean_resume = clean_text(resume_text)
        clean_job = clean_text(job_desc)

        emb_resume = model.encode([clean_resume])[0]
        emb_job = model.encode([clean_job])[0]

        score = compute_similarity(emb_resume, emb_job)

        resume_skills = extract_skills(clean_resume)
        job_skills = extract_skills(clean_job)

        missing_skills = list(set(job_skills) - set(resume_skills))

        st.subheader("Match Score")
        st.write(f"{round(score * 100, 2)}%")

        st.subheader("Resume Skills")
        st.write(resume_skills)

        st.subheader("Missing Skills")
        st.write(missing_skills)

        if missing_skills:
            st.subheader("Suggestions")
            st.write("Consider adding these skills if applicable:")
            st.write(missing_skills)
    else:
        st.warning("Please provide both resume and job description.")