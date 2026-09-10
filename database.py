import sqlite3


def create_table():
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            phone TEXT,
            skills TEXT,
            education TEXT,
            experience TEXT,
            match_score REAL,
            recommendation TEXT
        )
    """)

    conn.commit()
    conn.close()


def candidate_exists(email):
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM candidates
        WHERE email = ?
    """, (email,))

    candidate = cursor.fetchone()

    conn.close()

    return candidate is not None


def save_resume(
    email,
    phone,
    skills,
    education,
    experience,
    match_score,
    recommendation
):
    if candidate_exists(email):
        return False

    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO candidates (
            email,
            phone,
            skills,
            education,
            experience,
            match_score,
            recommendation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        email,
        phone,
        ", ".join(skills),
        ", ".join(education),
        ", ".join(experience),
        match_score,
        recommendation
    ))

    conn.commit()
    conn.close()

    return True


def get_all_resumes():
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            email,
            phone,
            skills,
            education,
            experience,
            match_score,
            recommendation
        FROM candidates
        ORDER BY match_score DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def clear_all_resumes():
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM candidates
    """)

    conn.commit()
    conn.close()
