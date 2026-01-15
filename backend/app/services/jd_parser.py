import json
from .ollama import ollama_generate
from ..models import JDParsed

PROMPT = """You are extracting structured requirements from a Job Description.
Return ONLY valid JSON matching this schema:
{
  "must_have": [string],
  "nice_to_have": [string],
  "tools": [string],
  "responsibilities": [string],
  "phrases": [string]
}
Rules:
- Keep items short (1-4 words for skills/tools).
- Include exact JD phrases in "phrases" when important.
- Do not add anything not implied by the JD.
JD:
"""

def parse_jd(jd_text: str) -> JDParsed:
    raw = ollama_generate(PROMPT + jd_text)
    # harden: extract first JSON object
    start = raw.find("{")
    end = raw.rfind("}")
    data = json.loads(raw[start:end+1])
    return JDParsed(**data)
