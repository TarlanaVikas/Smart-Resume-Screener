import re


def extract_name(text):
    lines = text.strip().split("\n")

    if lines:
        return lines[0].strip()

    return "Not Found"


def extract_email(text):
    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if match:
        return match.group()

    return "Not Found"


def extract_phone(text):
    match = re.search(
        r"(?<!\d)(?:\+91[-\s]?)?[6-9]\d{9}(?!\d)",
        text
    )

    if match:
        return match.group()

    return "Not Found"


def extract_skills(text):
    skill_list = [
        "Python",
        "Java",
        "C",
        "C++",
        "SQL",
        "HTML",
        "CSS",
        "JavaScript",
        "Machine Learning",
        "Deep Learning",
        "Data Science",
        "TensorFlow",
        "Keras",
        "OpenCV",
        "YOLO",
        "AWS",
        "Flask",
        "FastAPI",
        "React",
        "MongoDB",
        "MySQL",
        "SQLite",
        "Git",
        "GitHub"
    ]

    text_lower = text.lower()

    return [
        skill for skill in skill_list
        if skill.lower() in text_lower
    ]


def extract_education(text):
    education_keywords = [
        "B.Tech",
        "B.E",
        "Bachelor",
        "M.Tech",
        "M.E",
        "Master",
        "Computer Science",
        "Engineering",
        "University"
    ]

    text_lower = text.lower()

    return [
        keyword for keyword in education_keywords
        if keyword.lower() in text_lower
    ]


def extract_experience(text):
    experience_keywords = [
        "Internship",
        "Intern",
        "Experience",
        "Project",
        "Projects",
        "Developer",
        "Engineer"
    ]

    text_lower = text.lower()

    return [
        keyword for keyword in experience_keywords
        if keyword.lower() in text_lower
    ]
