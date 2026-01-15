import React from "react";
import type { ATSReport as ATSReportType } from "../api";

export default function ATSReport({ report }: { report: ATSReportType }) {
  const score = report.score;

  return (
    <div className="card">
      <h2>ATS Report</h2>

      <div className="scoreRow">
        <div className="score">{score}</div>
        <div className="scoreText">
          <div className="muted">Score (heuristic)</div>
          <div className="small">
            Missing keywords, repetition, and low quantification reduce score.
          </div>
        </div>
      </div>

      <div className="grid2">
        <div>
          <h3>Missing keywords</h3>
          {report.missing_keywords?.length ? (
            <ul className="list">
              {report.missing_keywords.slice(0, 12).map((k) => (
                <li key={k}>{k}</li>
              ))}
            </ul>
          ) : (
            <div className="muted">None 🎉</div>
          )}
        </div>

        <div>
          <h3>Repetition flags</h3>
          {report.repetition_flags?.length ? (
            <ul className="list">
              {report.repetition_flags.map((k) => (
                <li key={k}>{k}</li>
              ))}
            </ul>
          ) : (
            <div className="muted">No repetition issues detected</div>
          )}
        </div>
      </div>

      <div className="divider" />

      <div>
        <h3>Quantification gaps</h3>
        {report.quant_gaps?.length ? (
          <ul className="list">
            {report.quant_gaps.slice(0, 10).map((g) => (
              <li key={g}>{g}</li>
            ))}
          </ul>
        ) : (
          <div className="muted">Good quant coverage</div>
        )}
      </div>
    </div>
  );
}
