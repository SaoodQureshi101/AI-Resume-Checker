JOB_KEYWORDS = {
    "Data Analyst": ["sql", "python", "data", "excel", "data analysis"],
    "Junior Software Developer": ["python", "java", "c", "javascript", "html", "css"],
    "Network Technician": ["network", "routing", "switching", "ccna", "tcp"],
    "Help Desk Technician": ["help desk", "support", "troubleshoot", "windows", "linux", "remote desktop"],
    "CRM Administrator": ["salesforce", "crm"],
    "IT Support Specialist": ["hardware", "software", "imaging", "ticketing", "customer support"]
}


def suggest_jobs_from_text(text):
    """Return a list of suggested jobs ranked by keyword matches in the provided text."""
    text_l = text.lower()
    scores = []
    for job, keywords in JOB_KEYWORDS.items():
        score = 0
        for k in keywords:
            if k in text_l:
                score += 1
        if score > 0:
            scores.append((job, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return [job for job, _ in scores]
