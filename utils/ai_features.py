import re
import io
from sklearn.metrics.pairwise import cosine_similarity
from .skill_extraction import SKILL_KEYWORDS, extract_skills
from .job_suggester import suggest_jobs_from_text

SALARY_ESTIMATES = {
    "Data Analyst": (50000, 80000),
    "Junior Software Developer": (55000, 90000),
    "Network Technician": (45000, 70000),
    "Help Desk Technician": (35000, 60000),
    "CRM Administrator": (50000, 85000),
    "IT Support Specialist": (40000, 70000)
}


def _to_numpy(vec):
    try:
        # torch tensor
        import torch

        if hasattr(vec, 'detach'):
            return vec.detach().cpu().numpy()
    except Exception:
        pass
    try:
        return vec.numpy()
    except Exception:
        return vec


def simple_semantic_rewrite(resume_text, target_job=None):
    """Lightweight rewrite: strengthen verbs and add role-related phrases."""
    # basic verb upgrades
    upgrades = {
        r"contributed to": "implemented",
        r"assisted with": "developed and maintained",
        r"supported": "managed",
        r"worked with": "configured and supported",
        r"helped": "improved"
    }
    out = resume_text
    for k, v in upgrades.items():
        out = re.sub(k, v, out, flags=re.IGNORECASE)
    if target_job:
        out = out + f"\n\nTargeted for: {target_job}. Focused on user support, troubleshooting, and reliable system operation."
    return out


def interview_qa_simulator(resume_text, job_desc=None):
    """Generate likely interview questions and model answers from skills and experiences."""
    skills = extract_skills(resume_text)
    questions = []
    answers = []

    skill_answer_templates = {
        "sql": "I have built and optimized SQL queries for reporting and analytics, designed and maintained documentation, and ensured data accuracy when solving {skill}-related challenges.",
        "python": "I have developed Python scripts and applications to automate workflows, analyze data, and integrate APIs; I also wrote tests and used standard libraries to create maintainable solutions.",
        "java": "I have implemented Java services with object-oriented design, built unit-tested modules, and collaborated on code reviews to ensure performance and reliability in real-world projects.",
        "excel": "I have used Excel to perform data analysis, pivot table reporting, and process automation with formulas and macros to produce clean insights.",
        "javascript": "I have built frontend and backend components, worked with DOM APIs and node.js tooling, and translated requirements into responsive, modular code.",
    }

    for s in skills[:10]:
        q = f"Can you describe your experience with {s}?"
        key = s.lower().strip()
        template = skill_answer_templates.get(key)
        if template is None:
            template = "I have practical experience with {skill}, where I used it to solve problems and deliver reliable, repeatable results in team contexts."
        a = template.format(skill=s)
        questions.append(q)
        answers.append(a)

    # add experience prompts from meaningful lines only
    ex_lines = [l.strip() for l in re.split(r"\n|\.|;", resume_text) if l.strip()]
    seen = set()
    alt_responses = [
        "I focused on clear communication and measurable outcomes while driving the task to completion.",
        "I prioritized collaboration and data-driven decisions to meet project requirements on time.",
        "I worked closely with stakeholders to align execution with expected business value.",
    ]
    for i, ex in enumerate(ex_lines):
        if len(ex) < 20 or "expected" in ex.lower() or "gpa" in ex.lower():
            continue
        short = ex[:60].rstrip()
        if short in seen:
            continue
        seen.add(short)
        q = f"Tell me about a time you {short}..."
        a = f"In that role, I {ex}. {alt_responses[i % len(alt_responses)]}"
        questions.append(q)
        answers.append(a)
        if len(questions) >= 15:
            break

    return list(zip(questions, answers))


def skill_gap_and_learning_path(resume_text, job_desc):
    job_skills = extract_skills(job_desc or "")
    resume_skills = extract_skills(resume_text)
    missing = list(set(job_skills) - set(resume_skills))
    resources_map = {
        "sql": "Take a SQL fundamentals course (e.g., Mode SQL, SoloLearn)",
        "python": "Complete Python for Everybody or Automate the Boring Stuff",
        "docker": "Try Docker for Developers (Play with Docker tutorials)",
        "aws": "AWS Cloud Practitioner Essentials",
        "salesforce": "Trailhead path for Salesforce Administrator"
    }
    learning = [resources_map.get(s, f"Search for beginner courses on {s}") for s in missing]
    return {"missing_skills": missing, "learning_path": learning}


def company_targeted_tailoring(resume_text, company, job_desc=None):
    # simple heuristic: add a line mentioning company and align skills
    suggested = f"Experienced professional excited to contribute to {company}."
    if job_desc:
        # extract top keywords from job_desc
        jd_skills = extract_skills(job_desc)
        if jd_skills:
            suggested += " Key skills: " + ", ".join(jd_skills)
    tailored = resume_text + "\n\n" + suggested
    cover_delta = f"I am excited about {company} because of its focus on innovation and user-centered solutions."
    return {"tailored_resume": tailored, "cover_paragraph": cover_delta}


def explainable_match_report(model, resume_text, job_desc):
    # split into sentences
    sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', resume_text) if s.strip()]
    if not sents:
        return []
    try:
        emb_sents = model.encode(sents)
        emb_job = model.encode([job_desc])[0]
        emb_sents_np = _to_numpy(emb_sents)
        emb_job_np = _to_numpy(emb_job)
    except Exception:
        return []
    sims = cosine_similarity(emb_sents_np.reshape(len(sents), -1), emb_job_np.reshape(1, -1)).flatten()
    ranked = sorted(zip(sents, sims.tolist()), key=lambda x: x[1], reverse=True)
    return ranked


def resume_pdf_bytes(resume_text, title="Resume"):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except Exception:
        return None
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, title)
    y -= 30
    c.setFont("Helvetica", 10)
    lines = resume_text.splitlines()
    for line in lines:
        if y < 40:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)
        c.drawString(50, y, line[:100])
        y -= 14
    c.save()
    buffer.seek(0)
    return buffer.read()


def chatbot_response(user_input, resume_text):
    # naive assistant: if asks to 'rewrite' call semantic rewriter
    if "rewrite" in user_input.lower() or "improve" in user_input.lower():
        return simple_semantic_rewrite(resume_text, None)
    if "suggest" in user_input.lower() and "skills" in user_input.lower():
        skills = extract_skills(resume_text)
        return f"I recommend emphasizing: {', '.join(skills[:10])}"
    return "I can help rewrite the resume, suggest skills, or simulate interview Q&A. Try: 'Rewrite my resume' or 'Simulate interview'."


from .salary_api import fetch_average_wage


def extract_interview_questions(resume_text, job_desc=None):
    skills = extract_skills(resume_text)
    questions = [f"Describe a project where you used {s}." for s in skills[:8]]
    if job_desc:
        job_skills = extract_skills(job_desc)
        questions += [f"How does your experience with {jp} apply to this role?" for jp in job_skills[:5]]
    return questions


def generate_impact_bullets(resume_text):
    lines = [l.strip() for l in resume_text.splitlines() if l.strip()]
    bullets = []
    for l in lines[:8]:
        bullets.append(f"Improved {l} by 20% through optimization and testing.")
    if not bullets:
        bullets.append("Improved workflow efficiency by 20% through process automation.")
    return bullets


def standardize_job_title(title):
    mapping = {
        "dev": "Junior Software Developer",
        "developer": "Junior Software Developer",
        "help desk": "Help Desk Technician",
        "network": "Network Technician",
        "crm": "CRM Administrator"
    }
    t = title.lower()
    for key, out in mapping.items():
        if key in t:
            return out
    return title


def generate_email_followup(name, company, role):
    return (
        f"Hi {name},\n\nThank you for considering my application for {role} at {company}. "
        "I’m excited about the opportunity and would love to discuss how I can help your team succeed. "
        "Please let me know if you need any additional information.\n\nBest regards,\n[Your Name]"
    )


def suggest_roles_and_salary(resume_text, place="United States"):
    roles = suggest_jobs_from_text(resume_text)
    estimates = []
    for r in roles:
        market_wage = fetch_average_wage(r, place)
        if market_wage is not None:
            low = int(market_wage * 0.9)
            high = int(market_wage * 1.1)
            estimates.append({"role": r, "salary_range": (low, high), "source": "Data USA"})
        else:
            estimates.append({"role": r, "salary_range": SALARY_ESTIMATES.get(r, (40000, 80000)), "source": "fallback"})
    return estimates
