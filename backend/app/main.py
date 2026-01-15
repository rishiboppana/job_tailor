from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from bson import ObjectId
from pathlib import Path
from .models import TailorRequest, CompileRequest, BulletPatch
from .services.jd_parser import parse_jd
from .services.retriever import retrieve_top_projects
from .services.rewriter import rewrite_bullets
from .services.ats import make_ats_report
from .db import templates, skills, runs
from .services.latex import inject_projects, build_final_tex

app = FastAPI()

# Mount static files for PDF serving
outputs_dir = Path("outputs") / "pdfs"
outputs_dir.mkdir(parents=True, exist_ok=True)
app.mount("/outputs", StaticFiles(directory=str(outputs_dir)), name="outputs")

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
    patches = []
    bullet_counter = 0
    
    for proj in top:
        original_bullets = [b["text"] for b in proj["bullets"]][:3]
        allowed_skills = proj.get("skills", [])
        rewritten = rewrite_bullets(original_bullets, allowed_skills, must_keywords)
        all_bullets.extend(rewritten)

        title_line = r"{\textbf{" + proj["title"] + r": }}\hfill \textit{\textbf{" + proj["date_range"] + r"}}"
        
        # Create patches for each bullet
        bullet_lines = []
        for orig, rew in zip(original_bullets, rewritten):
            bullet_id = f"{proj.get('key', 'proj')}_b{bullet_counter}"
            patches.append({
                "id": bullet_id,
                "project_key": proj.get("key", ""),
                "project_title": proj["title"],
                "project_date_range": proj.get("date_range", ""),
                "original": orig,
                "rewritten": rew
            })
            # Use rewritten for initial preview
            bullet_lines.append(rew)
            bullet_counter += 1
        
        slots.append({"title_line": title_line, "bullet_lines": bullet_lines})

    tex_out = inject_projects(tex, slots)

    # update skills block later; for now we keep it as-is (you can add dynamic skills next)
    full_text = tex_out  # simple proxy; later we’ll extract PDF text for real ATS parse
    ats = make_ats_report(full_text, parsed.must_have + parsed.tools, all_bullets)

    run_doc = {
        "jd_text": req.jd_text,
        "parsed": parsed.model_dump(),
        "selected_projects": [p.get("key") for p in top],
        "ats_report": ats.model_dump(),
        "output_tex": tex_out,
        "patches": patches
    }
    ins = await runs.insert_one(run_doc)

    return {
        "run_id": str(ins.inserted_id),
        "parsed": parsed,
        "ats": ats,
        "latex": tex_out,
        "patches": patches
    }
    ins = await runs.insert_one(run_doc)

    return {
        "run_id": str(ins.inserted_id),
        "parsed": parsed,
        "ats": ats,
        "latex": tex_out,
        "patches": patches
    }

@app.post("/api/tailor/compile")
async def compile_final(req: CompileRequest):
    """Build final LaTeX from user decisions (accept/reject/edit)"""
    try:
        run_id_obj = ObjectId(req.run_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid run_id format")
    
    run = await runs.find_one({"_id": run_id_obj})
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    tpl = await templates.find_one({"_id": run.get("template_id", "resume_template_v1")})
    if not tpl:
        raise HTTPException(status_code=404, detail="Template not found")
    
    base_tex = tpl["latex"]
    final_tex = build_final_tex(base_tex, req.patches)
    
    # Update run with final output
    await runs.update_one(
        {"_id": run_id_obj},
        {"$set": {"final_tex": final_tex, "compiled_patches": [p.model_dump() for p in req.patches]}}
    )
    
    return {"latex": final_tex, "run_id": req.run_id}

@app.get("/api/tailor/pdf/{run_id}")
async def get_pdf(run_id: str):
    """Get previously generated PDF"""
    try:
        run_id_obj = ObjectId(run_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid run_id format")
    
    pdf_path = outputs_dir / f"resume_{run_id}.pdf"
    if pdf_path.exists():
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"resume_{run_id}.pdf"
        )
    else:
        raise HTTPException(status_code=404, detail="PDF not found. Please generate it first.")

@app.post("/api/tailor/pdf")
async def generate_pdf(req: CompileRequest):
    """Generate PDF from LaTeX (requires pdflatex installed)"""
    import subprocess
    import tempfile
    import os
    import shutil
    from fastapi.responses import FileResponse
    from pathlib import Path
    
    try:
        run_id_obj = ObjectId(req.run_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid run_id format")
    
    run = await runs.find_one({"_id": run_id_obj})
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    tpl = await templates.find_one({"_id": run.get("template_id", "resume_template_v1")})
    if not tpl:
        raise HTTPException(status_code=404, detail="Template not found")
    
    base_tex = tpl["latex"]
    final_tex = build_final_tex(base_tex, req.patches)
    
    # Use the global outputs_dir
    pdf_dir = outputs_dir
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    pdf_filename = f"resume_{req.run_id}.pdf"
    pdf_path = pdf_dir / pdf_filename
    tex_path = pdf_dir / f"resume_{req.run_id}.tex"
    
    # Write LaTeX file
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(final_tex)
    
    # Try to compile to PDF (requires pdflatex)
    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(pdf_dir), str(tex_path)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(pdf_dir)
        )
        
        # Run twice for proper references
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(pdf_dir), str(tex_path)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(pdf_dir)
        )
        
        if pdf_path.exists():
            # Return URL instead of file for frontend to use
            return {"pdf_url": f"/outputs/{pdf_filename}", "run_id": req.run_id}
        else:
            error_msg = result.stderr[:500] if result.stderr else result.stdout[:500]
            raise HTTPException(
                status_code=500,
                detail=f"PDF compilation failed. pdflatex output: {error_msg}"
            )
    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="pdflatex not found. Please install LaTeX distribution (e.g., TeX Live, MiKTeX)"
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="PDF compilation timed out")
