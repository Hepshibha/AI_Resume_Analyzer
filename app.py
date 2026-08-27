import streamlit as st

from resume_analyzer import (
    extract_text_from_pdf,
    extract_skills,
    calculate_skill_match,
    calculate_text_similarity,
    calculate_final_score
)

st.title("🤖 AI Resume Analyzer")

st.write(
    "Upload your resume and enter a job description "
    "to analyze your suitability for the role."
)

resume_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=250
)

if st.button("Analyze Resume"):

    if resume_file is None:
        st.warning("Please upload a resume.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        resume_text = extract_text_from_pdf(resume_file)

        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)

        if not resume_text.strip():
            st.error("No text could be extracted from the PDF.")
            st.stop()

        skill_score, matching_skills = calculate_skill_match(
            resume_skills,
            job_skills
        )

        similarity_score = calculate_text_similarity(
            resume_text,
            job_description
        )

        final_score = calculate_final_score(
            skill_score,
            similarity_score
        )

        missing_skills = [
            skill
            for skill in job_skills
            if skill not in resume_skills
        ]

        st.subheader("📊 Resume Analysis")

        st.metric(
            "Overall Match",
            f"{final_score}%"
        )

        st.write("### ✅ Matching Skills")

        if matching_skills:
            for skill in matching_skills:
                st.write(f"✓ {skill}")
        else:
            st.write("No matching skills found.")

        st.write("### ❌ Missing Skills")

        if missing_skills:
            for skill in missing_skills:
                st.write(f"• {skill}")
        else:
            st.write("No major missing skills detected.")

        st.write("### 📈 Analysis")

        st.write(f"Skill Match: {skill_score}%")
        st.write(f"Resume-Job Similarity: {similarity_score}%")