import re
import nltk
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer, util
import language_tool_python
import pdfplumber
from docx import Document

# ---------- NLTK SETUP (run once in env) ----------
# nltk.download('punkt')
# nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

# ---------- MODELS (load once) ----------
similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
tool = language_tool_python.LanguageTool('en-US')

# ---------- FILE TEXT EXTRACTION ----------
def extract_text(file, file_type):
    if file_type == "pdf":
        with pdfplumber.open(file) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif file_type == "docx":
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    return ""

# ---------- CLEAN SKILL EXTRACTION ----------
def extract_skills(text):
    text = text.lower()

    TECH_SKILLS = {
        "python", "java", "javascript", "django", "flask", "react", "node",
        "html", "css", "bootstrap", "tailwind", "sql", "mysql", "postgresql",
        "mongodb", "docker", "kubernetes", "aws", "azure", "git",
        "rest", "api", "graphql", "pandas", "numpy", "scikit-learn",
        "tensorflow", "pytorch"
    }

    SOFT_SKILLS = {
        "communication", "teamwork", "leadership",
        "problem solving", "time management", "critical thinking"
    }

    extracted = set()

    for skill in TECH_SKILLS | SOFT_SKILLS:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            extracted.add(skill.title())

    return sorted(extracted)

# ---------- RESUME PARSER ----------
def parse_resume(text):
    return {
        "skills": extract_skills(text),
        "experience": [],
        "education": []
    }

# ---------- GRAMMAR CHECK ----------
def check_grammar(text):
    matches = tool.check(text)
    errors = [
        f"{m.rule_id}: {m.message} (at '{m.context[:50]}...')"
        for m in matches
    ]
    count = len(matches)
    score = max(100 - count * 4, 20)
    return count, errors[:12], score

# ---------- FORMATTING CHECK ----------
def check_formatting(text):
    issues = []
    word_count = len(text.split())

    if word_count > 800:
        issues.append(f"Too long ({word_count} words)")
    if not re.search(r"(skills?|technical skills?)", text, re.I):
        issues.append("Missing 'Skills' section")
    if not re.search(r"(experience|work experience)", text, re.I):
        issues.append("Missing 'Experience' section")

    bullets = len(re.findall(r"^[•\-\*]\s|\s[•\-\*]\s", text, re.M))
    if bullets < 6:
        issues.append("Use more bullet points for readability")

    score = max(100 - len(issues) * 18, 30)
    return score, issues

# ---------- JOB RELEVANCE ----------
def analyze_relevance(resume_text, job_desc):
    if not job_desc.strip():
        return 0, [], []

    resume_emb = similarity_model.encode(resume_text)
    job_emb = similarity_model.encode(job_desc)

    semantic_score = util.cos_sim(resume_emb, job_emb)[0][0].item() * 100

    job_words = set(re.findall(r"\b\w{3,}\b", job_desc.lower()))
    resume_words = set(re.findall(r"\b\w{3,}\b", resume_text.lower()))

    matching = list(job_words & resume_words)[:12]
    missing = list(job_words - resume_words)[:10]

    keyword_score = (len(matching) / len(job_words) * 100) if job_words else 0

    relevance_score = round(
        semantic_score * 0.6 + keyword_score * 0.4,
        1
    )

    return relevance_score, matching, missing

# ---------- SKILL GUIDANCE ----------
def skill_guidance(extracted_skills, missing_keywords):
    msg = []
    if missing_keywords:
        msg.append(f"Add these skills: {', '.join(missing_keywords[:6])}")
    if len(extracted_skills) < 5:
        msg.append("Add more relevant technical & soft skills")
    return "\n".join(msg) or "Skills section looks good!"

# ---------- OVERALL SCORE ----------
def calculate_overall_score(grammar, formatting, relevance):
    return round(
        relevance * 0.45 +
        grammar * 0.25 +
        formatting * 0.25 +
        10,
        1
    )

# ---------- MAIN ANALYSIS ----------
def perform_analysis(cv_file, job_desc=""):
    file_type = cv_file.name.split(".")[-1].lower()
    text = extract_text(cv_file, file_type)

    extracted = parse_resume(text)

    grammar_count, grammar_issues, grammar_score = check_grammar(text)
    format_score, format_issues = check_formatting(text)
    relevance_score, matching, missing = analyze_relevance(text, job_desc)

    overall_score = calculate_overall_score(
        grammar_score,
        format_score,
        relevance_score
    )

    skill_sugg = skill_guidance(extracted["skills"], missing)

    return {
        "overall_score": overall_score,
        "grammar": {
            "errors": grammar_count,
            "issues": grammar_issues,
            "score": grammar_score
        },
        "formatting": {
            "score": format_score,
            "issues": format_issues
        },
        "relevance": {
            "score": relevance_score,
            "matching": matching,
            "missing": missing
        },
        "skills": {
            "extracted": extracted["skills"],
            "suggestions": skill_sugg
        }
    }
