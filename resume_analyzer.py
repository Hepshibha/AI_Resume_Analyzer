import re
import fitz

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILL_ALIASES = {
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "JavaScript": ["javascript", "js"],
    "React": ["react", "reactjs", "react.js"],
    "Git": ["git"],
    "GitHub": ["github"],
    "Python": ["python"],
    "Java": ["java"],
    "SQL": ["sql"],
    "Node.js": ["node", "nodejs", "node.js"],
    "MongoDB": ["mongodb", "mongo db"],
    "Machine Learning": ["machine learning", "ml"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "AWS": ["aws"],
    "Docker": ["docker"],
    "Bootstrap": ["bootstrap"],
    "Tailwind CSS": ["tailwind", "tailwind css"],
    "REST API": ["rest api", "restful api", "api"],
    "Data Analysis": ["data analysis"],
    "Power BI": ["power bi"],
}


def extract_text_from_pdf(file):

    import fitz

    file.seek(0)

    pdf_bytes = file.read()

    pdf = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text("text")

    pdf.close()

    return text


def clean_text(text):
    text = text.lower()

    # Keep letters, numbers and spaces
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(text):
    text = clean_text(text)

    found_skills = []

    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            alias = clean_text(alias)

            # Check exact word/phrase
            pattern = r"\b" + re.escape(alias) + r"\b"

            if re.search(pattern, text):
                found_skills.append(skill)
                break

    return found_skills

def calculate_skill_match(resume_skills, job_skills):

    if not job_skills:
        return 0, []

    matching_skills = [
        skill for skill in job_skills
        if skill in resume_skills
    ]

    score = (
        len(matching_skills) /
        len(job_skills)
    ) * 100

    return round(score, 2), matching_skills


def calculate_text_similarity(resume_text, job_description):

    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    if not resume_text or not job_description:
        return 0

    documents = [
        resume_text,
        job_description
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    return round(
        similarity[0][0] * 100,
        2
    )


def calculate_final_score(
    skill_score,
    similarity_score
):

    return round(
        (skill_score * 0.6) +
        (similarity_score * 0.4),
        2
    )