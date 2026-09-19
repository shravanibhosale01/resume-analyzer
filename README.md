# AI Resume Analyzer

Upload a resume (PDF/DOCX) + a job description, and get a match analysis:
matched skills, missing skills, an overall match score, and concrete
suggestions to improve your fit for the role.

**100% free and local.** No API key, no paid services, no data leaves
your machine.

## How it works

- **Skill matching** uses [spaCy](https://spacy.io/)'s PhraseMatcher to
  detect known skills (Python, SQL, AWS, Machine Learning, etc.) as real
  tokenized phrases in both the resume and job description \u2014 not fragile
  text substring matching.
- **Semantic similarity** uses spaCy's word-vector model to compare the
  overall meaning of the resume against the job description, so related
  but differently-worded experience (e.g. "risk profiling" vs
  "delinquency analytics") still counts.
- **Overall Match score** blends the two, weighted by how many
  recognizable skills were found in the job description \u2014 so a JD with
  very few dictionary skills doesn't produce a misleading 100/100 score.

## Setup

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```

2. Install dependencies:
   ```
   python -m pip install -r requirements.txt
   ```

3. Download the spaCy language model (one-time, needs internet;
   runs fully offline after this):
   ```
   python -m spacy download en_core_web_md
   ```

4. Run the app:
   ```
   python -m streamlit run app.py
   ```

5. Open the local URL it prints (usually http://localhost:8501).

## Project structure

- `app.py` \u2014 Streamlit UI: uploads, button, results display
- `extract.py` \u2014 pulls text out of PDF/DOCX resumes
- `analyzer.py` \u2014 spaCy-based skill matching + semantic similarity scoring
- `skills_data.py` \u2014 dictionary of ~90 tech/soft skills and their aliases
- `requirements.txt` \u2014 dependencies

## Notes / next steps

- Currently only handles text-based PDFs (not scanned images) \u2014 add OCR
  (e.g. `pytesseract`) if you need that.
- To add more recognized skills, edit the `SKILL_ALIASES` dictionary in
  `skills_data.py`.
- To deploy free online: push to GitHub (already done \u2714\ufe0f), then deploy
  via [Streamlit Community Cloud](https://share.streamlit.io).
- Add ATS-style formatting checks (standard section headers, no
  tables/columns, no images) as a rule-based pass on
  `extract_resume_text`'s output for a closer match to the original
  project idea.
