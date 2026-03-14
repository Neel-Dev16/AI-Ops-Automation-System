import React, { useState } from "react";
import "./App.css";
import IncidentTable from "./components/IncidentTable";
import LogAnalyzer from "./components/LogAnalyzer";

const navItems = [
  { id: "overview", label: "Overview" },
  { id: "analyze", label: "Analyze Logs" },
  { id: "history", label: "Incident History" },
  { id: "validation", label: "Validation" },
];

export default function App() {
  const [incidentRefreshKey, setIncidentRefreshKey] = useState(0);
  const [activePage, setActivePage] = useState("overview");

  function handleAnalysisComplete() {
    setIncidentRefreshKey((currentValue) => currentValue + 1);
  }

  function renderPageContent() {
    if (activePage === "overview") {
      return (
        <section className="content-stack">
          <article className="panel">
            <h2>Overview</h2>
            <p>
              Monitor the AI Ops workflow from one place. Use the sidebar to
              analyze incoming logs, review saved incidents, and validate the
              mock pipeline behavior.
            </p>
          </article>

          <article className="panel panel-muted">
            <h3>Platform Snapshot</h3>
            <p>
              The backend stores incidents in SQLite, applies automation rules,
              and exposes APIs for analysis and status updates.
            </p>
          </article>
        </section>
      );
    }

    if (activePage === "analyze") {
      return (
        <article className="panel">
          <h2>Analyze Logs</h2>
          <p>
            Paste application logs and send them to the backend for incident
            analysis and automation metadata generation.
          </p>
          <LogAnalyzer onAnalysisComplete={handleAnalysisComplete} />
        </article>
      );
    }

    if (activePage === "history") {
      return (
        <article className="panel">
          <h2>Incident History</h2>
          <p>
            Review incidents created by the analysis pipeline and update their
            lifecycle status from the dashboard.
          </p>
          <IncidentTable refreshKey={incidentRefreshKey} />
        </article>
      );
    }

    return (
      <section className="content-stack">
        <article className="panel">
          <h2>Validation</h2>
          <p>
            Use the backend validation script to compare expected mock incident
            outputs against actual API results.
          </p>
        </article>

        <article className="panel panel-muted">
          <h3>Next Step</h3>
          <p>
            This section can later show validation metrics, pass rates, and
            sample-case summaries from the analysis pipeline.
          </p>
        </article>
      </section>
    );
  }

  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <p className="sidebar-kicker">AI Ops</p>
          <h1>Automation System</h1>
          <p className="sidebar-subtitle">
            Intelligent incident analysis and automation dashboard
          </p>
        </div>

        <nav className="sidebar-nav" aria-label="Dashboard navigation">
          {navItems.map((item) => (
            <button
              key={item.id}
              type="button"
              className={
                activePage === item.id ? "nav-item nav-item-active" : "nav-item"
              }
              onClick={() => setActivePage(item.id)}
            >
              {item.label}
            </button>
          ))}
        </nav>
      </aside>

      <main className="main-content">
        <header className="content-header">
          <h2>{navItems.find((item) => item.id === activePage)?.label}</h2>
          <p>Use the sidebar to switch between core AI Ops workflows.</p>
        </header>

        {renderPageContent()}
      </main>
    </div>
  );
}
