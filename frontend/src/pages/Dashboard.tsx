import React, { useMemo, useState } from "react";
import { runTailor } from "../api";
import type { TailorRunResponse } from "../api";

type Props = {
  onDone: (res: TailorRunResponse) => void;
};

const sampleJD = `Data Engineering Intern
Responsibilities:
- Build ETL pipelines and data models
- Work with Snowflake, Airflow, dbt
- Write Python and SQL, optimize performance
Requirements:
- Experience with data warehousing and orchestration
- Familiarity with AWS, Docker
`;

export default function Dashboard({ onDone }: Props) {
  const [jd, setJd] = useState(sampleJD);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const canRun = useMemo(() => jd.trim().length > 30, [jd]);

  async function handleRun() {
    setErr(null);
    setLoading(true);
    try {
      const res = await runTailor(jd);
      onDone(res);
    } catch (e: any) {
      setErr(e?.message ?? "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
      <h1>Paste Job Description</h1>
      <p className="muted">
        This generates a tailored LaTeX resume by selecting projects from MongoDB and rewriting bullets using Ollama.
      </p>

      <textarea
        className="textarea"
        value={jd}
        onChange={(e) => setJd(e.target.value)}
        placeholder="Paste the job description here..."
      />

      {err && <div className="errorBox">{err}</div>}

      <div className="row">
        <button className="btn" onClick={handleRun} disabled={!canRun || loading}>
          {loading ? "Running..." : "Generate Tailored Resume"}
        </button>
        <button className="btnSecondary" onClick={() => setJd(sampleJD)} disabled={loading}>
          Load Sample JD
        </button>
      </div>

      <div className="note">
        Backend endpoint: <code>POST /api/tailor/run</code>
      </div>
    </div>
  );
}
