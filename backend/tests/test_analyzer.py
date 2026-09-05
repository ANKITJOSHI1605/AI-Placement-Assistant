from app.analyzer import analyze_resume, extract_skills


RESUME = """
Ankit Joshi | ankit@example.com
Summary
Software developer building reliable applications.
Education
B.Tech Computer Science
Skills
Python, FastAPI, React, PostgreSQL, Docker, Git
Projects
Built and deployed an attendance platform used by 20 users.
Experience
Developed REST API features and improved response time by 25%.
"""


def test_analysis_finds_sections_and_skills():
    result = analyze_resume(RESUME, "Looking for Python React AWS SQL Docker skills")
    assert result["ats_score"] >= 70
    assert "python" in result["matched_skills"]
    assert "aws" in result["missing_skills"]
    assert result["match_percentage"] == 60


def test_analysis_recommends_missing_structure():
    result = analyze_resume("Developer familiar with Python and Git. " * 8)
    assert result["ats_score"] < 50
    assert any("Projects" in item for item in result["recommendations"])


def test_aliases_are_canonical_and_deduplicated():
    assert extract_skills("JS javascript React.js nodejs Postgres sklearn CPP DSA") == [
        "algorithms", "c++", "data structures", "javascript", "node.js",
        "postgresql", "react", "scikit-learn",
    ]


def test_language_boundaries():
    assert extract_skills("C++ C# JavaScript JavaBeans") == ["c++", "javascript"]
    assert extract_skills("C, Java") == ["c", "java"]


def test_title_only_uses_labelled_estimate():
    result = analyze_resume(RESUME, "software developer,ai engineer")
    assert result["match_basis"] == "role_estimate"
    assert result["match_percentage"] > 0
    assert "not employer requirements" in result["match_note"]
    assert result["ats_score"] == analyze_resume(RESUME)["ats_score"]


def test_explicit_requirements_not_expanded():
    result = analyze_resume(RESUME, "AI engineer with Python and Docker")
    assert result["match_basis"] == "explicit_skills"
    assert result["job_skills"] == ["docker", "python"]
    assert result["match_percentage"] == 100


def test_machine_learning_title():
    result = analyze_resume(RESUME, "machine learning engineer")
    assert result["match_basis"] == "role_estimate"
    assert "scikit-learn" in result["job_skills"]


def test_empty_or_unrecognized_description_is_not_zero_match():
    for job in ("", "   ", "motivated team player", "astronaut"):
        result = analyze_resume(RESUME, job)
        assert result["match_percentage"] is None
        assert result["match_basis"] == "unavailable"
        assert result["missing_skills"] == []


def test_real_zero_overlap_still_shows_zero():
    result = analyze_resume("Python developer", "Java Kubernetes")
    assert result["match_percentage"] == 0
    assert result["match_basis"] == "explicit_skills"
