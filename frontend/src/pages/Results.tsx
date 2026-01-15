import React, { useMemo, useState } from "react";
import type { TailorRunResponse, BulletPatch, CompileResponse } from "../api";
import { compileFinal } from "../api";
import ATSReport from "../components/ATSReport";
import LatexViewer from "../components/LatexViewer";
import KeywordChips from "../components/KeywordChips";
import ResumeReview from "../components/ResumeReview";
import PDFViewer from "../components/PDFViewer";

type Props = {
  result: TailorRunResponse;
  onBack: () => void;
};

export default function Results({ result, onBack }: Props) {
  const parsed = result.parsed;
  const ats = result.ats;
  const [patches, setPatches] = useState<BulletPatch[]>(result.patches || []);
  const [finalLatex, setFinalLatex] = useState<string | null>(null);
  const [compiling, setCompiling] = useState(false);
  const [compileError, setCompileError] = useState<string | null>(null);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [generatingPDF, setGeneratingPDF] = useState(false);

  const topKeywords = useMemo(() => {
    const all = [...parsed.must_have, ...parsed.tools, ...parsed.phrases];
    return Array.from(new Set(all)).slice(0, 24);
  }, [parsed]);

  const handleCompile = async () => {
    setCompiling(true);
    setCompileError(null);
    try {
      const response: CompileResponse = await compileFinal({
        run_id: result.run_id,
        patches: patches,
      });
      setFinalLatex(response.latex);
      setPdfUrl(null); // Reset PDF URL to trigger regeneration
    } catch (e: any) {
      setCompileError(e?.message ?? "Failed to compile resume");
    } finally {
      setCompiling(false);
    }
  };

  const handleGeneratePDF = async () => {
    if (!finalLatex) {
      alert("Please compile the resume first");
      return;
    }
    setGeneratingPDF(true);
    try {
      const res = await fetch("http://localhost:8000/api/tailor/pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          run_id: result.run_id,
          patches: patches,
        }),
      });

      if (!res.ok) {
        const error = await res.text();
        throw new Error(error || "PDF generation failed");
      }

      const data = await res.json();
      // Use the URL from the backend
      setPdfUrl(`http://localhost:8000${data.pdf_url}`);
    } catch (e: any) {
      alert(`PDF generation failed: ${e.message}`);
    } finally {
      setGeneratingPDF(false);
    }
  };

  const displayLatex = finalLatex || result.latex;

  return (
    <div>
      <div className="rowBetween" style={{ marginBottom: "20px" }}>
        <h1>Resume Review</h1>
        <button className="btnSecondary" onClick={onBack}>← New JD</button>
      </div>

      <div className="resultsGrid">
        <div className="left">
          <ATSReport report={ats} />

          <div className="card">
            <h2>Extracted Keywords</h2>
            <KeywordChips title="Must-have" items={parsed.must_have} />
            <KeywordChips title="Tools" items={parsed.tools} />
            <KeywordChips title="Phrases" items={parsed.phrases} />
            <div className="divider" />
            <KeywordChips title="Top Combined" items={topKeywords} />
          </div>

          <div className="card">
            <h2>Review & Edit Bullets</h2>
            <p className="muted small" style={{ marginBottom: "16px" }}>
              Accept rewritten bullets, reject to use originals, or edit manually.
            </p>
            <ResumeReview patches={patches} onPatchesChange={setPatches} />
            
            <div style={{ marginTop: "20px", paddingTop: "20px", borderTop: "1px solid #eee" }}>
              <button
                className="btn"
                onClick={handleCompile}
                disabled={compiling}
                style={{ width: "100%" }}
              >
                {compiling ? "Compiling..." : "Build Final Resume"}
              </button>
              {compileError && (
                <div className="errorBox" style={{ marginTop: "10px" }}>
                  {compileError}
                </div>
              )}
              {finalLatex && (
                <div style={{ marginTop: "10px", padding: "10px", background: "#d4edda", borderRadius: "6px", color: "#155724" }}>
                  ✓ Resume compiled successfully! Preview updated below.
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="right">
          {pdfUrl ? (
            <PDFViewer pdfUrl={pdfUrl} runId={result.run_id} />
          ) : (
            <>
              <div className="card" style={{ marginBottom: "16px" }}>
                <div className="rowBetween">
                  <h2>Resume Preview</h2>
                  <button
                    className="btn"
                    onClick={handleGeneratePDF}
                    disabled={!finalLatex || generatingPDF}
                  >
                    {generatingPDF ? "Generating PDF..." : "Generate PDF Preview"}
                  </button>
                </div>
                <p className="muted small" style={{ marginTop: "10px" }}>
                  {finalLatex
                    ? "Click 'Generate PDF Preview' to see the formatted resume"
                    : "Compile the resume first to enable PDF preview"}
                </p>
              </div>
              <LatexViewer 
                latex={displayLatex} 
                runId={result.run_id}
                patches={finalLatex ? patches : []}
              />
            </>
          )}
        </div>
      </div>
    </div>
  );
}
