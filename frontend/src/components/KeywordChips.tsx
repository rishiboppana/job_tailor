import React from "react";

export default function KeywordChips({ title, items }: { title: string; items: string[] }) {
  const list = items ?? [];
  return (
    <div className="chipBlock">
      <div className="chipTitle">{title}</div>
      <div className="chips">
        {list.length ? (
          list.map((x) => (
            <span key={`${title}-${x}`} className="chip">{x}</span>
          ))
        ) : (
          <span className="muted">—</span>
        )}
      </div>
    </div>
  );
}
