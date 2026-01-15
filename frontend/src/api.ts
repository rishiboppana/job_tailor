export async function runTailor(jd_text: string) {
    const res = await fetch("http://localhost:8000/api/tailor/run", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ jd_text, template_id: "resume_template_v1", top_k_projects: 3 })
    });
    return res.json();
  }
  