# AI-Resume-Checker
# AI Resume Analyzer & Job Match Assistant

## Abstract

This project focuses on building an AI-powered tool that helps job seekers understand how well their resume matches a specific job description. By analyzing the content of a resume and comparing it with job requirements, the system can identify relevant skills, highlight gaps, and provide suggestions to improve the resume.

## Problem

Many job applicants send out resumes without knowing whether their skills and experience actually align with what employers are looking for. As a result, they may receive fewer responses or miss opportunities simply because their resume does not clearly reflect the required qualifications.

## Solution

This project aims to create an intelligent assistant that can analyze resumes and compare them with job postings. The system will:

* identify key skills and qualifications in a resume
* compare them with the requirements listed in a job description
* calculate a similarity or match score
* highlight missing or underrepresented skills
* suggest ways the resume could be improved

## Methods

The system uses Natural Language Processing (NLP) techniques along with modern transformer-based models. Sentence-BERT will be used to generate semantic embeddings of resumes and job descriptions, allowing the system to measure how closely they match in meaning and content.

## Data Sources

The project will use publicly available datasets, including job description datasets from Kaggle and sample resume datasets used for research and machine learning experiments.

## AI technology used

This project uses sentence-transformers `all-MiniLM-L6-v2` to generate resume and job description embeddings and compute semantic similarity. The system uses a hybrid approach with keyword skill extraction and cosine similarity via scikit-learn. An optional AI feature set is built in `utils/ai_features.py` for conversational and guidance enhancements.

## Tools and Technologies

The implementation will be developed using:

* Python
* HuggingFace Transformers (Sentence-BERT)
* Streamlit (for the user interface)
* Scikit-learn
* PyPDF2 (resume PDF ingest)
* reportlab (optional PDF output)
* requests (Data USA API salary lookup)

## What has been built so far

- merged and fixed conflicting files
- basic resume vs job description analyzer with match score + missing skills
- resume / job skill extraction module
- PDF upload support with fallback processing
- composite mode structure: Analyze, Generate, Advanced
- Generate mode creates resume / cover letter skeleton from user inputs
- Advanced mode features:
  - Semantic Resume Rewriter
  - Interview Q&A Simulator
  - Skill Gap & Learning Path
  - Company-Targeted Tailoring
  - Explainable Match Report
  - Resume Formatting & PDF Export
  - Interactive Revision Chatbot
  - Role Suggestion + Salary Estimate
  - Q&A Skill Extractor
  - Impact Bullet Generator
  - Job Title Normalizer
  - Email / Follow-up Builder
  - A/B Resume Comparator
- UX improvements: white theme, motivational quotes, company logos, stickers, cards, tabs

## Specific AI components and usage

1. **Sentence-BERT (`all-MiniLM-L6-v2`)**
   - `models/embedding_model.py`
   - used for semantic encoding of resume and job description text
   - similarity scoring in `utils/similarity.py`
   - explainable match report ranking in `utils/ai_features.py`

2. **Skill extraction (rule-based)**
   - `utils/skill_extraction.py`
   - keyword matching from `SKILL_KEYWORDS`
   - used in analyzer for resume/job skills and in advanced features for gaps and role suggestions

3. **AI features (heuristics + embedding utilities)**
   - `utils/ai_features.py`
   - Semantic rewrite, interview Q&A, skill gap/path, company tailoring, chat assistant, role+salary suggestions

4. **Job suggester mapping**
   - `utils/job_suggester.py`
   - role suggestions from skill match and salary range estimation

5. **PDF support / formatting**
   - `utils/pdf_utils.py` (PyPDF2 PDF parsing)
   - `utils/ai_features.py` PDF generation via reportlab


## Notes

- This is essentially hybrid AI: deep semantic matching via Sentence-BERT + deterministic skill heuristics.
- The “advanced AI” features are implemented as intelligent patterns and transformations (not cloud LLM calls), which makes the app fast and local.



