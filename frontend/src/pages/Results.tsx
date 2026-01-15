import React, { useMemo } from "react";
import type { TailorRunResponse } from "../api";
import ATSReport from "../components/ATSReport";
import LatexViewer from "../components/LatexViewer";
import KeywordChips from "../components/KeywordChips";

type Props = {
  result: TailorRunResponse;
  onBack: () => void;
};

export default function Results({ result, onBack }: Props) {
  const parsed = result.parsed;
  const ats = result.ats;

  const topKeywords = useMemo(() => {
    const all = [...parsed.must_have, ...parsed.tools, ...parsed.phrases];
    // dedupe
    return Array.from(new Set(all)).slice(0, 24);
  }, [parsed]);

  return (
    <div className="resultsGrid">
      <div className="left">
        <div className="rowBetween">
          <h1>Results</h1>
          <button className="btnSecondary" onClick={onBack}>← New JD</button>
        </div>

        <ATSReport report={ats} />

        <div className="card">
          <h2>Extracted Keywords</h2>
          <KeywordChips title="Must-have" items={parsed.must_have} />
          <KeywordChips title="Tools" items={parsed.tools} />
          <KeywordChips title="Phrases" items={parsed.phrases} />
          <div className="divider" />
          <KeywordChips title="Top Combined (preview)" items={topKeywords} />
        </div>
      </div>

      <div className="right">
        <LatexViewer latex={result.latex} runId={result.run_id} />
      </div>
    </div>
  );
}
