from rapidfuzz import fuzz
from ..db import projects

def score_project(jd_keywords: list[str], proj: dict) -> float:
    # simple overlap + fuzzy boost
    proj_skills = [s.lower() for s in proj.get("skills", [])]
    score = 0.0
    for kw in jd_keywords:
        k = kw.lower()
        if k in proj_skills:
            score += 3
        else:
            score += max(fuzz.partial_ratio(k, " ".join(proj_skills)) - 80, 0) / 20
    return score

async def retrieve_top_projects(jd_keywords: list[str], k: int = 3) -> list[dict]:
    docs = await projects.find({}).to_list(length=200)
    ranked = sorted(docs, key=lambda p: score_project(jd_keywords, p), reverse=True)
    return ranked[:k]
