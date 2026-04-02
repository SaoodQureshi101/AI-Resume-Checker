def generate_resume_text(name, contact, education, skills, experiences):
    """Create a simple plain-text resume from provided fields."""
    lines = []
    lines.append(name.strip())
    if contact:
        lines.append(contact.strip())
    lines.append("")
    if education:
        lines.append("EDUCATION")
        lines.append(education.strip())
        lines.append("")
    if skills:
        lines.append("SKILLS")
        # accept comma or newline separated
        skills_list = [s.strip() for s in skills.replace("\n", ",").split(",") if s.strip()]
        lines.append(", ".join(skills_list))
        lines.append("")
    if experiences:
        lines.append("EXPERIENCE")
        exp_lines = [e.strip() for e in experiences.splitlines() if e.strip()]
        for e in exp_lines:
            lines.append(f"- {e}")
    return "\n".join(lines)


def generate_cover_letter(name, contact, job_title, company, experiences, skills, tone="Professional"):
    """Generate a simple cover letter tailored to job title and company."""
    greeting = f"Dear Hiring Manager at {company}," if company else "Dear Hiring Manager,"

    intro = (
        f"My name is {name}. I am writing to apply for the {job_title} position at {company}. "
        if job_title or company else f"My name is {name} and I am interested in opportunities at your company. "
    )

    skills_sentence = "I bring experience with "
    skills_list = [s.strip() for s in (skills or "").replace("\n", ",").split(",") if s.strip()]
    if skills_list:
        skills_sentence += ", ".join(skills_list[:6]) + ". "
    else:
        skills_sentence = "I bring relevant technical skills and a strong work ethic. "

    exp_lines = [e.strip() for e in (experiences or "").splitlines() if e.strip()]
    example_sentence = (
        f"In my recent role, {exp_lines[0]} " if exp_lines else "In my recent roles, I have worked on technical projects and user support. "
    )

    closing = "Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to your team."

    if tone == "Casual":
        sign_off = "Sincerely,"
    else:
        sign_off = "Kind regards,"

    parts = [greeting, "", intro, skills_sentence, example_sentence, "", closing, "", sign_off, name]
    return "\n".join([p for p in parts if p])
