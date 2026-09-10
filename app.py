import streamlit as st
import pymupdf
import pandas as pd

from resume_parser import (
    extract_email,
    extract_phone,
    extract_skills,
    extract_education,
    extract_experience
)

from llm_matcher import get_llm_match

from database import (
    create_table,
    save_resume,
    get_all_resumes,
    clear_all_resumes
)


# ------------------------------------------
# PAGE CONFIG
# ------------------------------------------

st.set_page_config(
    page_title="VECTOR // Candidate Screening System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------------------------------
# DATABASE
# ------------------------------------------

create_table()


# ------------------------------------------
# CUSTOM UI
# No HTML UI components are used here.
# Only the CSS block uses HTML syntax.
# This prevents Streamlit from displaying
# generated HTML as visible text.
# ------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Syne:wght@600;700;800;900&display=swap');

:root {
    --bg: #03060a;
    --panel: #071019;
    --panel-2: #091521;
    --cyan: #00f0ff;
    --lime: #10ffa0;
    --red: #ff0055;
    --text-bright: #e2f1f8;
    --text-sub: #a5c2d3;
    --muted: #718ea0;
    --muted-2: #4e6f80;
    --border: rgba(0,240,255,.25);
}

* {
    box-sizing: border-box;
}

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
}

.stApp {
    background:
        radial-gradient(circle at 86% 7%, rgba(0,240,255,.10), transparent 32%),
        radial-gradient(circle at 12% 88%, rgba(16,255,160,.055), transparent 34%),
        linear-gradient(rgba(0,240,255,.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,240,255,.025) 1px, transparent 1px),
        var(--bg);
    background-size: 100% 100%, 100% 100%, 42px 42px, 42px 42px;
    color: var(--text-bright);
}

.block-container {
    max-width: 1540px;
    padding: 2rem 3rem 5rem;
}

/* Hide Streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { background: transparent !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(3,8,15,.97) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

[data-testid="stSidebar"] * {
    color: #9ab4c4;
}

[data-testid="stSidebar"] [data-testid="stMetric"] {
    margin: 10px 0;
}

/* Headings & Captions */
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4,
.stMarkdown h5 {
    font-family: 'Syne', sans-serif !important;
    color: #ffffff !important;
}

.stCaption {
    color: var(--text-sub) !important;
}

[data-testid="stSidebar"] h3 {
    font-family: 'Syne', sans-serif !important;
    color: #dff7ff !important;
    letter-spacing: .04em;
}

/* Widget Labels (Form headers/field titles) */
[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] p {
    color: #c7e1f0 !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
}

/* Inputs & Textarea */
.stTextArea textarea,
.stTextInput input {
    background: rgba(2,6,12,.92) !important;
    color: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 16px rgba(0,240,255,.22) !important;
}

/* Visible placeholder styling */
.stTextArea textarea::placeholder,
.stTextInput input::placeholder {
    color: #648599 !important;
    opacity: 0.9 !important;
}

[data-baseweb="select"] > div {
    background: rgba(2,6,12,.88) !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 !important;
    color: #e2f1f8 !important;
}

/* File Uploader Dropzone */
[data-testid="stFileUploader"] {
    background: rgba(4,12,21,.85) !important;
    border: 1px dashed rgba(0,240,255,.45) !important;
    padding: 12px;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 22px rgba(0,240,255,.15);
}

[data-testid="stFileUploader"] section {
    background: transparent !important;
    border: 0 !important;
}

/* Dropzone text: instructions, format limits, icons */
[data-testid="stFileUploaderDropzone"] svg {
    fill: var(--cyan) !important;
    stroke: var(--cyan) !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] span {
    color: #d1e5f0 !important;
    font-weight: 500 !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #799bb0 !important;
}

/* Dropzone "Browse files" button */
[data-testid="stFileUploader"] button {
    background: rgba(0,240,255,.14) !important;
    border: 1px solid var(--cyan) !important;
    color: var(--cyan) !important;
    border-radius: 0 !important;
    font-weight: 600 !important;
    transition: 0.2s ease !important;
}

[data-testid="stFileUploader"] button:hover {
    background: var(--cyan) !important;
    color: #03060a !important;
}

/* Primary Action Buttons */
.stButton > button,
.stDownloadButton > button {
    min-height: 48px !important;
    border-radius: 0 !important;
    border: 1px solid var(--cyan) !important;
    background: linear-gradient(
        90deg,
        rgba(0,240,255,.14),
        rgba(16,255,160,.08)
    ) !important;
    color: var(--cyan) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
    transition: .2s ease !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: var(--cyan) !important;
    color: #03060a !important;
    box-shadow: 0 0 24px rgba(0,240,255,.38) !important;
    transform: translateY(-1px);
}

/* Metrics & General Cards */
[data-testid="stMetric"] {
    background: rgba(4,11,20,.78) !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 !important;
    padding: 14px !important;
}

[data-testid="stMetricLabel"] {
    color: #718ea0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: .72rem !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-family: 'Syne', sans-serif !important;
}

.stProgress > div > div > div > div {
    background: var(--cyan) !important;
}

hr {
    border-color: var(--border) !important;
}

[data-testid="stExpander"] {
    background: rgba(5,12,20,.72) !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
}

[data-testid="stAlert"] {
    border-radius: 0 !important;
}

/* Hero elements */
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(2.5rem, 5vw, 5.2rem) !important;
    line-height: .9 !important;
    font-weight: 900 !important;
    letter-spacing: -.045em !important;
    color: #ffffff !important;
    margin: .3rem 0 1rem !important;
}

.hero-title-accent {
    color: var(--cyan) !important;
}

.hero-kicker {
    color: var(--cyan) !important;
    font-size: .68rem !important;
    letter-spacing: .22em !important;
    font-weight: 700 !important;
}

.hero-copy {
    color: #8faec0 !important;
    font-size: .88rem !important;
    line-height: 1.75 !important;
    max-width: 650px !important;
}

.muted-line {
    color: var(--muted-2) !important;
    font-size: .68rem !important;
    letter-spacing: .08em !important;
}

@media (max-width: 800px) {
    .block-container {
        padding: 1.2rem 1rem 4rem;
    }
    .hero-title {
        font-size: 3rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------
# SIDEBAR
# ------------------------------------------

with st.sidebar:

    st.markdown("### VECTOR / CONTROL")

    st.caption(
        "AI-Powered Candidate Screening Workspace"
    )

    st.divider()

    data_sidebar = get_all_resumes()

    st.metric(
        "Total Resumes in Vault",
        len(data_sidebar)
    )

    shortlisted = sum(
        1
        for row in data_sidebar
        if len(row) > 6
        and str(row[6]).upper() == "SHORTLISTED"
    )

    st.metric(
        "Shortlisted Candidates",
        shortlisted
    )

    st.divider()

    st.markdown("**Screening Engine**")

    st.caption("• PDF & TXT Document Extraction")
    st.caption("• Automated Requirement Matching")
    st.caption("• SQLite Candidate Vault")

    st.divider()

    st.caption("Local & Secure Execution")


# ------------------------------------------
# HERO
# ------------------------------------------

hero_left, hero_right = st.columns(
    [2.05, 1],
    gap="large"
)

with hero_left:

    st.markdown(
        '<div class="hero-kicker">CANDIDATE INTELLIGENCE PLATFORM</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-title">Resume Screening<br>'
        '<span class="hero-title-accent">& Ranking</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-copy">'
        'Upload candidate resumes, paste the target job description, '
        'and evaluate candidates based on skills, education, and relevant '
        'match criteria.'
        '</div>',
        unsafe_allow_html=True
    )

with hero_right:

    st.markdown("### ENGINE STATUS")

    st.metric(
        "SYSTEM",
        "ACTIVE"
    )

    st.markdown(
        '<div class="muted-line">LOCAL & SECURE EXECUTION</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="muted-line">SQLITE IMMUTABLE VAULT READY</div>',
        unsafe_allow_html=True
    )


st.divider()


# ------------------------------------------
# STEP 01
# ------------------------------------------

st.markdown("### STEP 01  /  Upload Documents & Job Description")

left, right = st.columns(
    [1, 1.15],
    gap="large"
)


with left:

    st.markdown("#### Upload Resumes")

    uploaded_files = st.file_uploader(
        "Drop candidate resumes here (PDF or TXT)",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.caption(
            "Selected files: "
            + ", ".join(
                file.name
                for file in uploaded_files
            )
        )


with right:

    st.markdown("#### Job Description (JD)")

    job_description = st.text_area(
        "Paste the Job Description here",
        height=180,
        placeholder=(
            "Paste full job description, required skills, "
            "and qualifications here..."
        )
    )


st.write("")

analyze_button = st.button(
    "START SCREENING RESUMES  →",
    use_container_width=True
)


# ------------------------------------------
# PROCESS RESUMES
# ------------------------------------------

if analyze_button:

    if not uploaded_files:

        st.warning(
            "Please upload at least one candidate resume."
        )

    elif not job_description.strip():

        st.warning(
            "Please paste a job description to screen against."
        )

    else:

        st.markdown("### SCREENING RESULTS")

        st.caption(
            "SYNCHRONOUS PARSE"
        )

        progress_bar = st.progress(0)

        total_files = len(uploaded_files)

        for index, uploaded_file in enumerate(
            uploaded_files
        ):

            st.divider()

            st.markdown(
                f"#### CANDIDATE #{index + 1:02d}"
            )

            st.caption(
                uploaded_file.name
            )

            try:

                # ----------------------------------
                # READ FILE
                # ----------------------------------

                if uploaded_file.name.lower().endswith(".pdf"):

                    pdf = pymupdf.open(
                        stream=uploaded_file.read(),
                        filetype="pdf"
                    )

                    text = ""

                    for page in pdf:

                        text += page.get_text()

                    pdf.close()

                else:

                    text = uploaded_file.read().decode(
                        "utf-8",
                        errors="ignore"
                    )


                # ----------------------------------
                # PARSE RESUME
                # ----------------------------------

                email = extract_email(text) or "Not found"

                phone = extract_phone(text) or "Not found"

                skills = extract_skills(text) or []

                education = extract_education(text) or []

                experience = extract_experience(text) or []


                # ----------------------------------
                # MATCHING
                # ----------------------------------

                llm_result = get_llm_match(
                    text,
                    job_description
                )

                matching_skills = llm_result.get(
                    "matching_skills",
                    []
                )

                missing_skills = llm_result.get(
                    "missing_skills",
                    []
                )

                match_score = llm_result.get(
                    "match_score",
                    0
                )

                recommendation = llm_result.get(
                    "recommendation",
                    ""
                )

                justification = llm_result.get(
                    "justification",
                    ""
                )


                # ----------------------------------
                # SCORE CATEGORY
                # ----------------------------------

                if match_score >= 8:

                    score_category = "Strong Match"

                elif match_score >= 6:

                    score_category = "Good Match"

                elif match_score >= 4:

                    score_category = "Moderate Match"

                else:

                    score_category = "Weak Match"


                # ----------------------------------
                # SCORE + CANDIDATE INFORMATION
                # ----------------------------------

                score_col, info_col = st.columns(
                    [0.85, 2],
                    gap="large"
                )


                with score_col:

                    st.metric(
                        "MATCH SCORE",
                        f"{match_score}/10"
                    )

                    st.markdown(
                        f"**{score_category}**"
                    )

                    st.caption(
                        "DECISION"
                    )

                    if recommendation == "SHORTLISTED":

                        st.success(
                            recommendation
                        )

                    else:

                        st.error(
                            recommendation
                        )


                with info_col:

                    st.markdown(
                        "##### CANDIDATE INFORMATION"
                    )

                    info1, info2 = st.columns(2)

                    with info1:

                        st.caption(
                            "EMAIL ADDRESS"
                        )

                        st.write(email)

                        st.caption(
                            "PHONE NUMBER"
                        )

                        st.write(phone)

                    with info2:

                        st.caption(
                            "EDUCATION"
                        )

                        st.write(
                            ", ".join(education)
                            if education
                            else "Not detected"
                        )

                        st.caption(
                            "EXPERIENCE SUMMARY"
                        )

                        st.write(
                            ", ".join(experience)
                            if experience
                            else "Not detected"
                        )

                    st.caption(
                        "DETECTED SKILLS"
                    )

                    if skills:

                        st.write(
                            ", ".join(skills)
                        )

                    else:

                        st.write(
                            "None detected"
                        )


                # ----------------------------------
                # SKILL ANALYSIS
                # ----------------------------------

                st.write("")

                match_col, gap_col = st.columns(
                    2,
                    gap="large"
                )


                with match_col:

                    st.markdown(
                        "##### MATCHING REQUIREMENTS"
                    )

                    st.caption(
                        "Found in both candidate resume and job description"
                    )

                    if matching_skills:

                        st.write(
                            ", ".join(
                                matching_skills
                            )
                        )

                    else:

                        st.caption(
                            "No matching requirements identified"
                        )


                with gap_col:

                    st.markdown(
                        "##### MISSING SKILLS / GAPS"
                    )

                    st.caption(
                        "Required by role but not found in resume"
                    )

                    if missing_skills:

                        st.write(
                            ", ".join(
                                missing_skills
                            )
                        )

                    else:

                        st.caption(
                            "No critical capability gaps identified"
                        )


                # ----------------------------------
                # RECOMMENDATION
                # ----------------------------------

                st.markdown(
                    "##### RECOMMENDATION"
                )

                if recommendation == "SHORTLISTED":

                    st.success(
                        f"**SHORTLISTED:** {justification}"
                    )

                else:

                    st.error(
                        f"**NOT SHORTLISTED:** {justification}"
                    )


                # ----------------------------------
                # SAVE
                # ----------------------------------

                saved = save_resume(
                    email,
                    phone,
                    skills,
                    education,
                    experience,
                    match_score,
                    recommendation
                )


                if saved:

                    st.caption(
                        "Status: New candidate profile successfully "
                        "saved to database."
                    )

                else:

                    st.caption(
                        "Status: Candidate already exists in database "
                        "(duplicate prevented)."
                    )


                # ----------------------------------
                # RAW TEXT
                # ----------------------------------

                with st.expander(
                    "View Raw Extracted Resume Text"
                ):

                    st.text(text)


            except Exception as e:

                st.error(
                    f"Error processing {uploaded_file.name}: {e}"
                )


            progress_bar.progress(
                (index + 1) / total_files
            )


        st.success(
            "Screening completed for all uploaded resumes."
        )


# ------------------------------------------
# STEP 02
# ------------------------------------------

st.divider()

st.markdown(
    "### STEP 02  /  Candidate Vault & Rankings"
)

st.caption(
    "View, search, filter, and export all evaluated "
    "candidates stored in your database."
)


# ------------------------------------------
# DATABASE RESULTS
# ------------------------------------------

data = get_all_resumes()


if data:

    df = pd.DataFrame(
        data,
        columns=[
            "Email",
            "Phone",
            "Skills",
            "Education",
            "Experience",
            "Match Score",
            "Recommendation"
        ]
    )


    df = df.sort_values(
        by="Match Score",
        ascending=False
    ).reset_index(
        drop=True
    )


    df.insert(
        0,
        "Rank",
        range(1, len(df) + 1)
    )


    # --------------------------------------
    # FILTERS
    # --------------------------------------

    st.markdown("#### SEARCH & FILTER")

    f1, f2, f3 = st.columns(
        [2, 1, 1]
    )


    with f1:

        search_text = st.text_input(
            "Search Candidates",
            placeholder="Filter by email or skill..."
        )


    with f2:

        recommendation_filter = st.selectbox(
            "Filter by Decision",
            [
                "All",
                "SHORTLISTED",
                "NOT SHORTLISTED"
            ]
        )


    with f3:

        min_score = st.slider(
            "Minimum Score",
            min_value=0.0,
            max_value=10.0,
            value=0.0,
            step=0.5
        )


    # --------------------------------------
    # APPLY FILTERS
    # --------------------------------------

    filtered_df = df.copy()


    if recommendation_filter != "All":

        filtered_df = filtered_df[
            filtered_df["Recommendation"]
            .astype(str)
            .str.upper()
            ==
            recommendation_filter
        ]


    filtered_df = filtered_df[
        filtered_df["Match Score"]
        >=
        min_score
    ]


    if search_text.strip():

        search_lower = search_text.lower()

        filtered_df = filtered_df[
            filtered_df["Email"]
            .astype(str)
            .str.lower()
            .str.contains(
                search_lower,
                na=False
            )
            |
            filtered_df["Skills"]
            .astype(str)
            .str.lower()
            .str.contains(
                search_lower,
                na=False
            )
        ]


    filtered_df = filtered_df.reset_index(
        drop=True
    )


    if not filtered_df.empty:

        filtered_df["Rank"] = range(
            1,
            len(filtered_df) + 1
        )


        st.caption(
            f"Showing {len(filtered_df)} matching candidate(s)"
        )


        shortlist_df = filtered_df[
            [
                "Rank",
                "Email",
                "Skills",
                "Match Score",
                "Recommendation"
            ]
        ]


        st.dataframe(
            shortlist_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rank": st.column_config.NumberColumn(
                    "Rank",
                    width="small"
                ),
                "Match Score": st.column_config.ProgressColumn(
                    "Match Score",
                    min_value=0,
                    max_value=10,
                    format="%.1f / 10"
                )
            }
        )


        # ----------------------------------
        # EXPORT + CLEAR
        # ----------------------------------

        csv = shortlist_df.to_csv(
            index=False
        ).encode(
            "utf-8"
        )


        export_col, clear_col = st.columns(
            [3, 1]
        )


        with export_col:

            st.download_button(
                "Export Shortlist as CSV  ↓",
                data=csv,
                file_name="candidate_shortlist.csv",
                mime="text/csv",
                use_container_width=True
            )


        with clear_col:

            if st.button(
                "Clear All Records",
                use_container_width=True
            ):

                clear_all_resumes()

                st.rerun()


        with st.expander(
            "View Complete Candidate Details"
        ):

            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )


    else:

        st.warning(
            "No candidates match your current search and filter settings."
        )


else:

    st.info(
        "No candidates stored in the database yet. "
        "Upload resumes and run screening above."
    )


# ------------------------------------------
# FOOTER
# ------------------------------------------

st.divider()

st.caption(
    "VECTOR // RESUME SCREENING PLATFORM     "
    "LOCAL SYSTEM • 2026"
)
