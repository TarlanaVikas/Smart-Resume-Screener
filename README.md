<div align="center">

# ◈ VECTOR

### Smart Resume Screening & Candidate Intelligence

**Turn unstructured resumes into structured hiring signals.**

<br>

[![Python](https://img.shields.io/badge/Python-3.x-0b0f14?style=for-the-badge&logo=python&logoColor=00f0ff)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-0b0f14?style=for-the-badge&logo=streamlit&logoColor=ff4b4b)](https://streamlit.io/)
[![PyMuPDF](https://img.shields.io/badge/PyMuPDF-PDF%20Engine-0b0f14?style=for-the-badge&logo=adobeacrobatreader&logoColor=ff0055)](https://pymupdf.readthedocs.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Layer-0b0f14?style=for-the-badge&logo=pandas&logoColor=10ffa0)](https://pandas.pydata.org/)
[![SQLite](https://img.shields.io/badge/SQLite-Local%20Vault-0b0f14?style=for-the-badge&logo=sqlite&logoColor=00f0ff)](https://www.sqlite.org/)

<br>

![Status](https://img.shields.io/badge/STATUS-ACTIVE-10ffa0?style=flat-square)
![Interface](https://img.shields.io/badge/UI-HUD%20INTERFACE-00f0ff?style=flat-square)
![Storage](https://img.shields.io/badge/STORAGE-LOCAL%20SQLITE-ffaa00?style=flat-square)
![Privacy](https://img.shields.io/badge/DATA-LOCAL%20FIRST-ff0055?style=flat-square)

</div>

---

## `01 // SYSTEM OVERVIEW`

**VECTOR** is a Streamlit-based resume screening system designed to turn a collection of candidate resumes and a target job description into structured screening results.

Instead of manually opening resumes one by one, VECTOR creates a simple screening pipeline:

```text
RESUME
   │
   ▼
┌─────────────────┐
│ DOCUMENT PARSER │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ CANDIDATE DATA  │
│ Email / Phone   │
│ Skills / Edu.   │
│ Experience      │
└────────┬────────┘
         │
         │        JOB DESCRIPTION
         │               │
         └───────┬───────┘
                 ▼
        ┌─────────────────┐
        │ MATCHING ENGINE │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ SCORE + GAPS    │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ CANDIDATE VAULT │
        └─────────────────┘
````

The result is a ranked candidate workspace where recruiters can inspect match scores, matching skills, missing skills, candidate information, and stored screening results.

---

## `02 // WHAT IT DOES`

### ◇ Resume Intake

Upload one or multiple:

* PDF resumes
* TXT resumes

PDF content is extracted using **PyMuPDF**.

### ◇ Candidate Extraction

VECTOR identifies:

* Email
* Phone number
* Skills
* Education keywords
* Experience-related keywords

### ◇ Job Matching

The screening engine compares the candidate resume against the supplied job description.

It identifies:

```text
MATCHING SKILLS
        +
MISSING SKILLS
        ↓
   MATCH SCORE
```

The current matching engine uses a predefined technical-skills vocabulary and calculates a score from `0–10`.

### ◇ Screening Decision

Candidates are classified as:

```text
7.0 ───────────────► SHORTLISTED
0.0 ───────────────► NOT SHORTLISTED
```

The system also provides a short justification for the recommendation.

### ◇ Candidate Vault

Evaluated candidates are stored locally in SQLite.

The vault supports:

* Ranking
* Search
* Recommendation filtering
* Minimum score filtering
* Complete candidate details
* CSV export
* Clearing stored candidates

---

## `03 // THE INTERFACE`

VECTOR is intentionally designed as a **command-center style screening workspace** rather than a conventional dashboard.

The interface uses:

```text
DARK SYSTEM CANVAS
       +
CYAN SIGNALS
       +
LIME STATUS STATES
       +
CRIMSON GAP STATES
       +
MONOSPACE TELEMETRY
```

The goal is to make the screening process feel like an analytical workstation rather than another form-heavy HR application.

---

## `04 // SCREENING PIPELINE`

### STEP 01 — Upload

Provide candidate resumes.

```text
PDF / TXT
   ↓
Text Extraction
```

### STEP 02 — Define Role

Paste the target job description.

```text
JOB DESCRIPTION
        ↓
Required Skill Detection
```

### STEP 03 — Analyze

VECTOR evaluates every uploaded resume.

```text
Candidate Resume
       │
       ├── Contact Extraction
       ├── Skill Extraction
       ├── Education Detection
       ├── Experience Detection
       │
       └── Requirement Matching
                 │
                 ▼
              SCORE
```

### STEP 04 — Rank

Candidates are automatically ordered by match score.

### STEP 05 — Filter

Use the candidate vault to narrow results by:

* Email
* Skill
* Recommendation
* Minimum score

### STEP 06 — Export

Download the filtered shortlist as CSV.

---

## `05 // ARCHITECTURE`

```text
                 ┌─────────────────────┐
                 │      Streamlit      │
                 │       app.py        │
                 └──────────┬──────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
       ┌────────────┐ ┌─────────────┐ ┌────────────┐
       │   Parser   │ │   Matcher   │ │  Database  │
       │ resume_    │ │ llm_matcher │ │ database.py│
       │ parser.py  │ │    .py      │ │            │
       └────────────┘ └─────────────┘ └─────┬──────┘
                                            │
                                            ▼
                                      ┌────────────┐
                                      │  SQLite    │
                                      │ resumes.db │
                                      └────────────┘
```

### Components

| Component          | Responsibility                           |
| ------------------ | ---------------------------------------- |
| `app.py`           | Streamlit interface and application flow |
| `resume_parser.py` | Candidate information extraction         |
| `llm_matcher.py`   | Resume/JD skill matching and scoring     |
| `database.py`      | SQLite candidate storage                 |
| `requirements.txt` | Python dependencies                      |
| `resumes.db`       | Local runtime database                   |

---

## `06 // PROJECT STRUCTURE`

```text
smart-resume-screener/
│
├── app.py
├── resume_parser.py
├── llm_matcher.py
├── database.py
├── requirements.txt
├── .gitignore
│
└── resumes.db
       └── generated locally
```

`resumes.db` is intentionally excluded from version control.

---

## `07 // GET STARTED`

### 1. Clone

```bash
git clone https://github.com/TarlanaVikas/smart-resume-screener.git
cd smart-resume-screener
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Current dependencies are:

```text
streamlit
pymupdf
pandas
```

### 4. Launch VECTOR

```bash
streamlit run app.py
```

The application will open in your browser.

---

## `08 // DATABASE MODEL`

Candidate records are stored locally in SQLite.

```text
candidates
│
├── id
├── email
├── phone
├── skills
├── education
├── experience
├── match_score
└── recommendation
```

The database automatically prevents duplicate candidates based on email.

---

## `09 // SCORING LOGIC`

The matching engine maintains a predefined technical skill vocabulary.

For each skill:

```text
Resume contains skill?
          │
          ├── YES ──┐
          │         │
          ▼         ▼
     JD contains?   MATCH
          │
          └── NO
```

Required skills are divided into:

```text
MATCHING SKILLS
+
MISSING SKILLS
=
TOTAL REQUIRED
```

The score is calculated as:

```text
Match Score =
(Matching Skills / Total Required Skills) × 10
```

Example:

```text
Required skills     : 5
Candidate matches   : 4

Score = (4 / 5) × 10

Score = 8.0 / 10
```

A score of `7.0` or above results in:

```text
SHORTLISTED
```

Otherwise:

```text
NOT SHORTLISTED
```

---

## `10 // LOCAL-FIRST DESIGN`

VECTOR does not require an external AI API key for its current matching implementation.

The repository uses a local processing flow:

```text
Resume
  ↓
PyMuPDF
  ↓
Parser
  ↓
Matching Engine
  ↓
SQLite
```

This makes the project straightforward to run locally and suitable for experimentation without configuring an external model API.

---

## `11 // WHY VECTOR?`

Most resume-screening interfaces try to look like conventional HR dashboards.

VECTOR takes a different direction.

```text
Traditional
───────────
Forms
Tables
Cards
Charts

VECTOR
──────
Signals
Telemetry
Candidate dossiers
Skill gaps
Screening states
Local candidate vault
```

The interface is built around the idea of a **candidate intelligence console**.

---

## `12 // CURRENT CAPABILITIES`

```text
[✓] Multi-resume upload
[✓] PDF parsing
[✓] TXT parsing
[✓] Email extraction
[✓] Phone extraction
[✓] Skill extraction
[✓] Education detection
[✓] Experience detection
[✓] Job-description matching
[✓] Match scoring
[✓] Skill-gap analysis
[✓] Shortlist recommendation
[✓] SQLite persistence
[✓] Duplicate prevention
[✓] Candidate ranking
[✓] Candidate search
[✓] Score filtering
[✓] Recommendation filtering
[✓] CSV export
```

---

## `13 // ROADMAP`

Possible future upgrades:

```text
[ ] DOCX resume support
[ ] Advanced semantic embeddings
[ ] Experience-in-years extraction
[ ] Resume ranking analytics
[ ] Candidate comparison mode
[ ] Recruiter authentication
[ ] Role-specific scoring profiles
[ ] Resume improvement suggestions
[ ] Interview question generation
[ ] Bias-aware screening controls
[ ] Cloud deployment
```

---

## `14 // PRIVACY NOTE`

Candidate resumes may contain sensitive personal information.

VECTOR stores screening records in a local SQLite database during execution. The repository intentionally excludes `resumes.db` through `.gitignore`.

Do not commit real candidate resumes, personal information, credentials, or private recruitment data to a public repository.

---

## `15 // TECH STACK`

```text
┌─────────────────────────────────────────┐
│                 VECTOR                  │
├─────────────────────────────────────────┤
│ Language        Python                  │
│ Interface       Streamlit               │
│ PDF Engine      PyMuPDF                 │
│ Data Processing Pandas                  │
│ Database        SQLite                  │
│ Matching        Rule-based skill engine │
└─────────────────────────────────────────┘
```

---

## `16 // RUN LOCALLY`

```bash
git clone https://github.com/TarlanaVikas/smart-resume-screener.git

cd smart-resume-screener

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
```

---

## `17 // REPOSITORY`

**Source**

[https://github.com/TarlanaVikas/smart-resume-screener](https://github.com/TarlanaVikas/smart-resume-screener)

---

<div align="center">

### VECTOR // CANDIDATE INTELLIGENCE

`PARSE → MATCH → SCORE → RANK`

<br>

Built with Python + Streamlit

**© 2026 Vikas Tarlana**

</div>
```
