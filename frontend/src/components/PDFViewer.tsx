import { useState, useEffect } from "react";

type Props = {
  pdfUrl: string | null;
  runId: string;
};

export default function PDFViewer({ pdfUrl, runId }: Props) {
  const [error, setError] = useState<string | null>(null);

  if (!pdfUrl) {
    return (
      <div className="card">
        <h2>PDF Preview</h2>
        <p className="muted small">
          Compile the resume to generate PDF preview. PDF generation requires pdflatex on the server.
        </p>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="rowBetween">
        <h2>Resume PDF Preview</h2>
        <a
          href={pdfUrl}
          download={`resume_${runId}.pdf`}
          className="btn"
          style={{ textDecoration: "none", display: "inline-block" }}
        >
          Download PDF
        </a>
      </div>
      <div style={{ marginTop: "16px", border: "1px solid #e6e6e6", borderRadius: "8px", overflow: "hidden" }}>
        <iframe
          src={pdfUrl}
          style={{
            width: "100%",
            height: "800px",
            border: "none",
          }}
          title="PDF Preview"
          onError={() => setError("Failed to load PDF preview")}
        />
        {error && (
          <div className="errorBox" style={{ margin: "16px" }}>
            {error}
          </div>
        )}
      </div>
    </div>
  );
}

