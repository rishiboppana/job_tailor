import React, { useState } from "react";
import Dashboard from "./pages/Dashboard";
import Results from "./pages/Results";
import type { TailorRunResponse } from "./api";

export default function App() {
  const [result, setResult] = useState<TailorRunResponse | null>(null);

  return (
    <div className="appShell">
      <header className="header">
        <div className="brand">Job Tailor (Local)</div>
        <div className="sub">FastAPI + React + MongoDB Atlas + Ollama</div>
      </header>

      <main className="main">
        {!result ? (
          <Dashboard onDone={setResult} />
        ) : (
          <Results result={result} onBack={() => setResult(null)} />
        )}
      </main>

      <footer className="footer">
        <span>Tip: keep Ollama running at http://localhost:11434</span>
      </footer>
    </div>
  );
}
