import json
from .ollama import ollama_generate

PROMPT = """Rewrite resume bullets to better match the JD keywords.
Return ONLY JSON:
{{ "bullets": ["string", "string", "string"] }}

Constraints:
- Do NOT invent tools/skills not present in AllowedSkills.
- Do NOT invent metrics; keep existing metrics only.
- Each bullet: 1 sentence, action verb first, include 1–2 keywords naturally.
- Avoid repetition of starting verbs.
- IMPORTANT: Wrap important keywords, tools, skills, and metrics in LaTeX bold: \\textbf{{keyword}}
- Preserve any existing \\textbf{{}} formatting from original bullets.

AllowedSkills: {allowed_skills}
JDKeywords: {jd_keywords}

OriginalBullets:
{bullets}
"""

def rewrite_bullets(
    original_bullets: list[str],
    allowed_skills: list[str],
    jd_keywords: list[str],
) -> list[str]:

    prompt = PROMPT.format(
        allowed_skills=", ".join(allowed_skills),
        jd_keywords=", ".join(jd_keywords),
        bullets="\n".join(f"- {b}" for b in original_bullets),
    )

    raw = ollama_generate(prompt)

    # --- SAFETY PARSE ---
    start = raw.find("{")
    end = raw.rfind("}")

    if start == -1 or end == -1 or end <= start:
        # fallback: return original bullets unchanged
        return original_bullets

    try:
        data = json.loads(raw[start:end + 1])
        bullets = data.get("bullets", [])
        if not bullets or not isinstance(bullets, list):
            return original_bullets
        return bullets
    except Exception:
        return original_bullets
