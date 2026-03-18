import React, { useState } from "react";
import "./App.css";
import IncidentTable from "./components/IncidentTable";
import LogAnalyzer from "./components/LogAnalyzer";
import OverviewDashboard from "./components/OverviewDashboard";

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
      return <OverviewDashboard refreshKey={incidentRefreshKey} />;
    }

    if (activePage === "analyze") {
      return (
        <article className="panel">
          <h2>Analyze Logs</h2>
          <LogAnalyzer onAnalysisComplete={handleAnalysisComplete} />
        </article>
      );
    }

    if (activePage === "history") {
      return (
        <article className="panel">
          <h2>Incident History</h2>
          <IncidentTable refreshKey={incidentRefreshKey} />
        </article>
      );
    }

    return (
      <section className="content-stack">
        <article className="panel">
          <h2>Validation</h2>
        </article>

        <article className="panel panel-muted">
          <h3>Next Step</h3>
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
        </header>

        {renderPageContent()}
      </main>
    </div>
  );
}
