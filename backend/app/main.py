from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import TailorRequest
from .services.jd_parser import parse_jd
from .services.retriever import retrieve_top_projects
from .services.rewriter import rewrite_bullets
from .services.ats import make_ats_report
from .db import templates, skills, runs
from .services.latex import inject_projects, replace_block

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/tailor/run")
async def tailor_run(req: TailorRequest):
    parsed = parse_jd(req.jd_text)
    must_keywords = parsed.must_have + parsed.tools + parsed.phrases

    tpl = await templates.find_one({"_id": req.template_id})
    tex = tpl["latex"]

    # store new skills as unmapped (safe)
    for kw in parsed.must_have + parsed.tools:
        await skills.update_one(
            {"name": kw},
            {"$setOnInsert": {"name": kw, "status": "unmapped", "synonyms": []}},
            upsert=True
        )

    top = await retrieve_top_projects(parsed.must_have + parsed.tools, k=req.top_k_projects)

    slots = []
    all_bullets = []
    for proj in top:
        original = [b["text"] for b in proj["bullets"]][:3]
        allowed_skills = proj.get("skills", [])
        rewritten = rewrite_bullets(original, allowed_skills, must_keywords)
        all_bullets.extend(rewritten)

        title_line = r"{\textbf{" + proj["title"] + r": }}\hfill \textit{\textbf{" + proj["date_range"] + r"}}"
        slots.append({"title_line": title_line, "bullets": rewritten})

    tex_out = inject_projects(tex, slots)

    # update skills block later; for now we keep it as-is (you can add dynamic skills next)
    full_text = tex_out  # simple proxy; later we’ll extract PDF text for real ATS parse
    ats = make_ats_report(full_text, parsed.must_have + parsed.tools, all_bullets)

    run_doc = {
        "jd_text": req.jd_text,
        "parsed": parsed.model_dump(),
        "selected_projects": [p.get("key") for p in top],
        "ats_report": ats.model_dump(),
        "output_tex": tex_out
    }
    ins = await runs.insert_one(run_doc)

    return {"run_id": str(ins.inserted_id), "parsed": parsed, "ats": ats, "latex": tex_out}
