import { useState } from "react";
import type { BulletPatch } from "../api";

function downloadTextFile(filename: string, content: string) {
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

async function downloadPDF(runId: string, patches: BulletPatch[]) {
  try {
    const res = await fetch("http://localhost:8000/api/tailor/pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ run_id: runId, patches }),
    });

    if (!res.ok) {
      const error = await res.text();
      throw new Error(error || "PDF generation failed");
    }

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `resume_${runId}.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  } catch (e: any) {
    alert(`PDF download failed: ${e.message}`);
  }
}

type Props = {
  latex: string;
  runId: string;
  patches?: BulletPatch[];
};

export default function LatexViewer({ latex, runId, patches = [] }: Props) {
  const [downloadingPDF, setDownloadingPDF] = useState(false);

  const handleDownloadPDF = async () => {
    if (patches.length === 0) {
      alert("Please compile the resume first before downloading PDF");
      return;
    }
    setDownloadingPDF(true);
    try {
      await downloadPDF(runId, patches);
    } finally {
      setDownloadingPDF(false);
    }
  };

  return (
    <div className="card">
      <div className="rowBetween">
        <h2>Resume Preview</h2>
        <div className="row">
          <button
            className="btnSecondary"
            onClick={() => navigator.clipboard.writeText(latex)}
          >
            Copy LaTeX
          </button>
          <button
            className="btnSecondary"
            onClick={() => downloadTextFile(`tailored_${runId}.tex`, latex)}
          >
            Download .tex
          </button>
          {patches.length > 0 && (
            <button
              className="btn"
              onClick={handleDownloadPDF}
              disabled={downloadingPDF}
            >
              {downloadingPDF ? "Generating..." : "Download PDF"}
            </button>
          )}
        </div>
      </div>

      <p className="muted small" style={{ marginTop: "10px" }}>
        {patches.length > 0
          ? "PDF generation requires pdflatex on the server. Download .tex to compile locally."
          : "Build final resume to enable PDF download."}
      </p>

      <textarea className="textarea mono" value={latex} readOnly style={{ marginTop: "12px" }} />
    </div>
  );
}
