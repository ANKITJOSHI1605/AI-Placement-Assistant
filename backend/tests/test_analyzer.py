from app.analyzer import analyze_resume


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

