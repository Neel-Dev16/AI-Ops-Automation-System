import React from "react";
import "./App.css";

export default function App() {
  return (
    <main className="app-shell">
      <section className="hero">
        <h1>AI Ops Automation System</h1>
        <p>
          Intelligent incident analysis and automation dashboard
        </p>
      </section>

      <section className="panel-grid">
        <article className="panel">
          <h2>Dashboard</h2>
          <p>
            This area will show incident summaries, severity trends, and
            automation activity.
          </p>
          <ul>
            <li>Recent incidents</li>
            <li>Severity overview</li>
            <li>Automation actions</li>
          </ul>
        </article>

        <article className="panel">
          <h2>Analyze Logs</h2>
          <p>
            This section will allow users to paste raw logs and trigger backend
            analysis.
          </p>
          <ul>
            <li>Raw log input</li>
            <li>Mock LLM analysis results</li>
            <li>Generated incident details</li>
          </ul>
        </article>
      </section>
    </main>
  );
}
