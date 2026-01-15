import React from "react";

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

export default function LatexViewer({ latex, runId }: { latex: string; runId: string }) {
  return (
    <div className="card">
      <div className="rowBetween">
        <h2>Generated LaTeX</h2>
        <div className="row">
          <button
            className="btnSecondary"
            onClick={() => navigator.clipboard.writeText(latex)}
          >
            Copy
          </button>
          <button
            className="btn"
            onClick={() => downloadTextFile(`tailored_${runId}.tex`, latex)}
          >
            Download .tex
          </button>
        </div>
      </div>

      <p className="muted small">
        Next step (backend upgrade): compile .tex → PDF and show preview here.
      </p>

      <textarea className="textarea mono" value={latex} readOnly />
    </div>
  );
}
