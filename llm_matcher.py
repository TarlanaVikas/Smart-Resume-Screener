def get_llm_match(resume_text, job_description):
    skills_database = [
        "Python",
        "Java",
        "C",
        "C++",
        "Machine Learning",
        "Deep Learning",
        "Computer Vision",
        "OpenCV",
        "YOLO",
        "TensorFlow",
        "Keras",
        "SQL",
        "AWS",
        "HTML",
        "CSS",
        "Git",
        "Data Structures",
        "Algorithms"
    ]

    resume_lower = resume_text.lower()
    job_lower = job_description.lower()

    matching_skills = [
        skill for skill in skills_database
        if skill.lower() in resume_lower and skill.lower() in job_lower
    ]

    missing_skills = [
        skill for skill in skills_database
        if skill.lower() in job_lower and skill.lower() not in resume_lower
    ]

    total_required = len(matching_skills) + len(missing_skills)

    if total_required > 0:
        match_score = round(
            (len(matching_skills) / total_required) * 10,
            1
        )
    else:
        match_score = 0

    if match_score >= 7:
        recommendation = "SHORTLISTED"
        justification = (
            "The candidate matches most of the important "
            "skills required for this job."
        )
    else:
        recommendation = "NOT SHORTLISTED"
        justification = (
            "The candidate is missing several important "
            "skills required for this job."
        )

    return {
        "match_score": match_score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "recommendation": recommendation,
        "justification": justification
    }
