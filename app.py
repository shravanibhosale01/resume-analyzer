"""
AI Resume Analyzer - FREE version (no API key, no paid services).
Upload a resume + paste a job description, get a skill-matching +
semantic similarity based analysis, fully local using spaCy.

Run with: streamlit run app.py
"""

import streamlit as st
from extract import extract_resume_text
from analyzer import analyze_resume

st.set_page_config(page_title="AI Resume Analyzer", page_icon="\U0001F4C4", layout="wide")

st.title("\U0001F4C4 AI Resume Analyzer")
st.caption(
    "Upload your resume and a job description to see how well you match "
    "\u2014 and how to improve. 100% free, runs locally, no API key needed."
)

with st.sidebar:
    st.header("How it works")
    st.markdown(
        "1. Upload your resume (PDF or DOCX)\n"
        "2. Paste the job description\n"
        "3. Click Analyze\n"
        "4. Get matched skills, gaps, and suggestions"
    )
    st.markdown("---")
    st.caption(
        "This runs entirely on your machine using spaCy's NLP model \u2014 "
        "skills are matched as real tokenized phrases (not fragile text "
        "substrings), and the overall score uses semantic similarity, so "
        "related-but-differently-worded experience still counts. No data "
        "leaves your computer, no API costs."
    )

col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Resume")
    resume_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

with col2:
    st.subheader("Job Description")
    jd_text = st.text_area("Paste the job description here", height=280)

analyze_clicked = st.button("Analyze \U0001F50D", type="primary", use_container_width=True)

if analyze_clicked:
    if not resume_file:
        st.error("Please upload a resume file.")
    elif not jd_text.strip():
        st.error("Please paste a job description.")
    else:
        try:
            with st.spinner("Extracting resume text..."):
                resume_text = extract_resume_text(resume_file)

            with st.spinner("Analyzing match (loading NLP model on first run)..."):
                result = analyze_resume(resume_text, jd_text)

            st.success("Analysis complete!")

            if result.get("low_confidence"):
                st.warning(
                    "Only a couple of recognizable skill keywords were found in "
                    "this job description, so the keyword score below is based "
                    "on a very small sample \u2014 the Overall Match score accounts "
                    "for this by leaning more on semantic similarity."
                )

            st.markdown("---")

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Overall Match", f"{result.get('overall_score', 0)}/100")
            m2.metric("Keyword Match", f"{result.get('keyword_match_score', 0)}/100")
            m3.metric("Semantic Similarity", f"{result.get('semantic_similarity_score', 0)}/100")
            m4.metric("Relevance", result.get("experience_relevance", "N/A"))

            st.markdown("---")

            r1, r2 = st.columns(2)
            with r1:
                st.subheader("\u2705 Matched Skills")
                matched = result.get("matched_skills", [])
                if matched:
                    st.markdown(", ".join(f"`{s}`" for s in matched))
                else:
                    st.write("None detected from the skills dictionary.")

            with r2:
                st.subheader("\u274C Missing Skills")
                missing = result.get("missing_skills", [])
                if missing:
                    st.markdown(", ".join(f"`{s}`" for s in missing))
                else:
                    st.write("None \u2014 great coverage!")

            st.markdown("---")
            st.subheader("\U0001F4CB Notes")
            st.write(result.get("experience_notes", ""))

            st.markdown("---")
            st.subheader("\U0001F4A1 Suggestions to Improve Your Match")
            for i, suggestion in enumerate(result.get("suggestions", []), 1):
                st.write(f"{i}. {suggestion}")

            with st.expander("View raw extracted resume text"):
                st.text(resume_text)

        except RuntimeError as e:
            st.error(str(e))
        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.markdown("---")
st.caption("Built with Streamlit + spaCy. Fully local \u2014 nothing is uploaded anywhere.")
