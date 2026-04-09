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

The implementation wasdeveloped using:

* Python
* HuggingFace Transformers (Sentence-BERT)
* Streamlit (for the user interface)
* Scikit-learn
* PyPDF2 (resume PDF ingest)
* reportlab (optional PDF output)
* requests (Data USA API salary lookup)


## How to Run

### 1) Open the project folder

Use PowerShell and move into the project directory:

```powershell
cd "C:\Users\1\OneDrive\Desktop\ai-resume-analyzer"
```

### 2) Create and activate a virtual environment (first time)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run this once and then activate again:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3) Install dependencies

```powershell
pip install -r requirements.txt
```

### 4) Run the app

```powershell
streamlit run app.py
```

### 5) Open in browser

Streamlit will print a local URL (usually `http://localhost:8501`). Open it in your browser.

### Common issue

Do not run this app with `python app.py`. This project is a Streamlit app and should be started with `streamlit run app.py`.

## Notes

- This is essentially hybrid AI: deep semantic matching via Sentence-BERT + deterministic skill heuristics.
- The “advanced AI” features are implemented as intelligent patterns and transformations (not cloud LLM calls), which makes the app fast and local.

## link to youtube video

https://youtu.be/LdeJYbPsJ9o



