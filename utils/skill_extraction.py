SKILL_KEYWORDS = [
    "python", "java", "c++", "machine learning", "deep learning",
    "nlp", "tensorflow", "pytorch", "sql", "data analysis",
    "communication", "teamwork", "aws", "docker"
]


def extract_skills(text):
    found_skills = []
    text_lower = text.lower()
    for skill in SKILL_KEYWORDS:
        if skill in text_lower:
            found_skills.append(skill)
    return list(set(found_skills))