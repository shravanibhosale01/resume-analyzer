"""
Skills dictionary used with spaCy's PhraseMatcher.

Each canonical skill maps to a list of alias phrases that might appear in
a resume or job description (e.g. "ML" and "Machine Learning" both
resolve to the same canonical skill). Because PhraseMatcher tokenizes
these properly, "ts" won't falsely match inside "results" or "tests" the
way a naive regex substring search would.

Deliberately ambiguous single-word skills (bare "R", bare "Go", bare "C")
are either dropped or written as more specific phrases to avoid false
positives against common English words.
"""

SKILL_ALIASES = {
    # Programming languages
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript"],
    "C++": ["c++", "cpp"],
    "C#": ["c#", "csharp"],
    "Go": ["golang"],
    "Rust": ["rust"],
    "R": ["r programming", "r language"],
    "SQL": ["sql"],
    "PHP": ["php"],
    "Ruby": ["ruby"],
    "Swift": ["swift"],
    "Kotlin": ["kotlin"],
    "MATLAB": ["matlab"],
    "Scala": ["scala"],

    # Web / frameworks
    "React": ["react", "react.js", "reactjs"],
    "Angular": ["angular"],
    "Vue.js": ["vue.js", "vuejs", "vue"],
    "Node.js": ["node.js", "nodejs", "node"],
    "Django": ["django"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi"],
    "Spring Boot": ["spring boot", "spring framework"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "Streamlit": ["streamlit"],
    "Express.js": ["express.js", "expressjs"],
    "Next.js": ["next.js", "nextjs"],
    "REST APIs": ["rest api", "restful api", "rest apis"],

    # Data / ML / AI
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning", "dl"],
    "Natural Language Processing": ["natural language processing", "nlp"],
    "Computer Vision": ["computer vision"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Keras": ["keras"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Data Visualization": ["data visualization"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "Statistics": ["statistics", "statistical analysis"],
    "A/B Testing": ["a/b testing", "ab testing"],
    "LLM": ["large language model", "llm", "generative ai", "genai"],

    # Cloud / DevOps
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"],
    "GCP": ["google cloud", "gcp"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "CI/CD": ["ci/cd", "continuous integration", "continuous deployment"],
    "Jenkins": ["jenkins"],
    "Terraform": ["terraform"],
    "Linux": ["linux"],
    "Git": ["git"],
    "GitHub": ["github"],
    "GitLab": ["gitlab"],

    # Databases
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MongoDB": ["mongodb", "mongo"],
    "Redis": ["redis"],
    "SQLite": ["sqlite"],
    "Oracle DB": ["oracle database"],
    "NoSQL": ["nosql"],

    # Tools / methodology
    "Excel": ["excel"],
    "Jira": ["jira"],
    "Agile": ["agile"],
    "Scrum": ["scrum"],
    "Figma": ["figma"],
    "Postman": ["postman"],

    # Soft skills (lighter weight but often screened for)
    "Communication": ["communication skills", "communication"],
    "Leadership": ["leadership experience", "team leadership", "leading a team"],
    "Project Management": ["project management"],
    "Problem Solving": ["problem solving", "problem-solving"],
    "Teamwork": ["teamwork", "collaboration"],
}
