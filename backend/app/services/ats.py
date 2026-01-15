import re
from collections import Counter
from ..models import ATSReport

WEAK_VERBS = ["worked", "helped", "responsible", "assisted"]
ACTION_VERBS = ["Built", "Designed", "Implemented", "Optimized", "Developed", "Deployed", "Automated", "Improved"]

def keyword_missing(text: str, must_have: list[str]) -> list[str]:
    t = text.lower()
    return [k for k in must_have if k.lower() not in t]

def repetition_flags(bullets: list[str]) -> list[str]:
    first_words = []
    for b in bullets:
        m = re.match(r"^\W*([A-Za-z]+)", b.strip())
        if m:
            first_words.append(m.group(1).lower())
    c = Counter(first_words)
    return [w for w, n in c.items() if n >= 2]

def quant_gaps(bullets: list[str]) -> list[str]:
    gaps = []
    for i, b in enumerate(bullets, start=1):
        if not re.search(r"\d", b):
            gaps.append(f"Bullet {i} has no metric/number.")
    return gaps

def score(missing: list[str], reps: list[str], gaps: list[str]) -> int:
    s = 100
    s -= min(40, 5 * len(missing))
    s -= min(20, 5 * len(reps))
    s -= min(20, 3 * len(gaps))
    return max(0, s)

def make_ats_report(full_text: str, must_have: list[str], all_bullets: list[str]) -> ATSReport:
    missing = keyword_missing(full_text, must_have)
    reps = repetition_flags(all_bullets)
    gaps = quant_gaps(all_bullets)
    return ATSReport(score=score(missing, reps, gaps), missing_keywords=missing, repetition_flags=reps, quant_gaps=gaps)
