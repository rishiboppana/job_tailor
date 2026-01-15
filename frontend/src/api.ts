export type JDParsed = {
  must_have: string[];
  nice_to_have: string[];
  tools: string[];
  responsibilities: string[];
  phrases: string[];
};

export type ATSReport = {
  score: number;
  missing_keywords: string[];
  repetition_flags: string[];
  quant_gaps: string[];
};

export type TailorRunResponse = {
  run_id: string;
  parsed: JDParsed;
  ats: ATSReport;
  latex: string;
};

const API_BASE = "http://localhost:8000";

export async function runTailor(jd_text: string): Promise<TailorRunResponse> {
  const res = await fetch(`${API_BASE}/api/tailor/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      jd_text,
      template_id: "resume_template_v1",
      top_k_projects: 3,
    }),
  });

  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`Backend error ${res.status}: ${txt}`);
  }
  return res.json();
}
