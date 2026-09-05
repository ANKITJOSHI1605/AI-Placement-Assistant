import re
from collections import Counter


SKILLS = {
    "python", "java", "javascript", "typescript", "c++", "c", "sql",
    "react", "node.js", "express", "fastapi", "flask", "django", "spring boot",
    "postgresql", "mysql", "mongodb", "redis", "docker", "kubernetes",
    "aws", "azure", "git", "github", "linux", "rest api", "machine learning",
    "deep learning", "tensorflow", "pytorch", "scikit-learn", "pandas",
    "data structures", "algorithms", "html", "css", "tailwind"
}

SECTION_PATTERNS = {
    "summary": r"\b(summary|profile|objective)\b",
    "education": r"\b(education|academic)\b",
    "experience": r"\b(experience|employment|internship)\b",
    "projects": r"\b(projects?|personal projects?)\b",
    "skills": r"\b(technical skills?|skills?|technologies)\b",
}

# Conservative aliases: do not infer SQL from PostgreSQL or C from C++.
ALIASES = {
    "javascript": ("js",), "typescript": ("ts",),
    "node.js": ("nodejs", "node js"), "react": ("reactjs", "react.js"),
    "postgresql": ("postgres",), "scikit-learn": ("sklearn", "scikit learn"),
    "machine learning": ("ml",), "deep learning": ("dl",),
    "rest api": ("rest apis", "restful api", "restful apis"),
    "c++": ("cpp",), "data structures": ("dsa",),
    "algorithms": ("dsa",), "tailwind": ("tailwindcss", "tailwind css"),
}
ROLE_SKILLS = {
    "software developer": {"git", "data structures", "algorithms", "sql"},
    "software engineer": {"git", "data structures", "algorithms", "sql"},
    "ai engineer": {"python", "machine learning", "deep learning"},
    "machine learning engineer": {"python", "machine learning", "scikit-learn"},
    "frontend developer": {"html", "css", "javascript", "git"},
    "backend developer": {"rest api", "sql", "git"},
}


def contains_phrase(text: str, phrase: str) -> bool:
    return bool(re.search(rf"(?<![\w+#]){re.escape(phrase)}(?![\w+#])", text))


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_skills(text: str) -> list[str]:
    normalized = normalize(text)
    return sorted(skill for skill in SKILLS
                  if any(contains_phrase(normalized, alias)
                         for alias in (skill, *ALIASES.get(skill, ()))))


def analyze_resume(text: str, job_description: str = "") -> dict:
    clean_text = text.strip()
    normalized = normalize(clean_text)
    resume_skills = extract_skills(clean_text)
    job_skills = extract_skills(job_description)
    normalized_job = normalize(job_description)
    roles = [role for role in ROLE_SKILLS if contains_phrase(normalized_job, role)]
    # Only use a role baseline for short prompts without explicit skill requirements.
    title_only = bool(roles) and len(normalized_job.split()) <= 12
    if title_only:
        remaining = normalized_job
        for role in sorted(roles, key=len, reverse=True):
            remaining = remaining.replace(role, " ")
        title_only = not extract_skills(remaining)
    if title_only:
        job_skills = sorted(set().union(*(ROLE_SKILLS[role] for role in roles)))
        match_basis = "role_estimate"
        match_note = "Estimated against a generic role baseline, not employer requirements. Paste the full job description for a specific comparison."
    elif job_skills:
        match_basis = "explicit_skills"
        match_note = "Keyword overlap with recognized skills in the job description; not a hiring probability."
    else:
        match_basis = "unavailable"
        match_note = "Paste a job description containing specific skills to calculate a match."
    matched = sorted(set(resume_skills) & set(job_skills))
    missing = sorted(set(job_skills) - set(resume_skills))
    found_sections = [name for name, pattern in SECTION_PATTERNS.items() if re.search(pattern, normalized)]

    section_score = round(len(found_sections) / len(SECTION_PATTERNS) * 30)
    skills_score = min(30, len(resume_skills) * 3)
    contact_score = 10 if re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", clean_text) else 0
    impact_terms = re.findall(r"\b(?:built|developed|improved|reduced|increased|designed|implemented|deployed|led)\b", normalized)
    impact_score = min(15, len(impact_terms) * 3)
    measurable_score = 10 if re.search(r"\b\d+(?:\.\d+)?%|\b\d+\+?\s+(?:users?|projects?|requests?|hours?)\b", normalized) else 0
    length_score = 5 if 150 <= len(clean_text.split()) <= 1200 else 2
    base_score = section_score + skills_score + contact_score + impact_score + measurable_score + length_score

    if job_skills and match_basis == "explicit_skills":
        match_ratio = len(matched) / len(job_skills)
        ats_score = round(base_score * 0.65 + match_ratio * 35)
    else:
        match_ratio = len(matched) / len(job_skills) if job_skills else 0
        ats_score = base_score

    recommendations = []
    if match_basis != "explicit_skills":
        recommendations.append(match_note)
    if "summary" not in found_sections:
        recommendations.append("Add a focused 2–3 line professional summary.")
    for section in ("experience", "projects", "skills"):
        if section not in found_sections:
            recommendations.append(f"Add a clearly labelled {section.title()} section.")
    if not impact_terms:
        recommendations.append("Start project and experience bullets with measurable action verbs.")
    if measurable_score == 0:
        recommendations.append("Quantify outcomes with percentages, users, latency, or other concrete results.")
    if missing:
        prefix = "Consider learning these role-baseline skills: " if match_basis == "role_estimate" else "Review these job skills not detected in your resume: "
        recommendations.append(prefix + ", ".join(missing[:8]) + ". Only add skills you genuinely have.")
    if not recommendations:
        recommendations.append("Strong structure—tailor the top skills and achievements for each application.")

    keyword_counts = Counter(re.findall(r"\b[a-z][a-z+#.]{2,}\b", normalized))
    return {
        "ats_score": min(100, ats_score),
        "word_count": len(clean_text.split()),
        "sections_found": found_sections,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percentage": round(match_ratio * 100) if job_skills else None,
        "match_basis": match_basis,
        "match_note": match_note,
        "top_keywords": [word for word, _ in keyword_counts.most_common(10)],
        "recommendations": recommendations,
    }
