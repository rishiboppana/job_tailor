from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class JDParsed(BaseModel):
    must_have: List[str] = []
    nice_to_have: List[str] = []
    tools: List[str] = []
    responsibilities: List[str] = []
    phrases: List[str] = []

class TailorRequest(BaseModel):
    jd_text: str
    template_id: str = "resume_template_v1"
    top_k_projects: int = 3

class Bullet(BaseModel):
    id: str
    text: str
    verified: bool = True
    metrics: List[str] = []

class Project(BaseModel):
    key: str
    title: str
    date_range: str
    skills: List[str] = []
    bullets: List[Bullet] = []

class ATSReport(BaseModel):
    score: int
    missing_keywords: List[str] = []
    repetition_flags: List[str] = []
    quant_gaps: List[str] = []

class BulletPatch(BaseModel):
    id: str
    project_key: str
    project_title: str
    project_date_range: Optional[str] = ""
    original: str
    rewritten: str
    accepted: Optional[bool] = None
    edited_text: Optional[str] = None

class CompileRequest(BaseModel):
    run_id: str
    patches: List[BulletPatch]
