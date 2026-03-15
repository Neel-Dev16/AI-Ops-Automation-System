import React, { useEffect, useState } from "react";

import { getIncidents } from "../api/incidents";

const kpiCards = [
  {
    key: "total",
    label: "Total Incidents",
    className: "kpi-card-total",
  },
  {
    key: "critical",
    label: "Critical",
    className: "kpi-card-critical",
  },
  {
    key: "high",
    label: "High Severity",
    className: "kpi-card-high",
  },
  {
    key: "open",
    label: "Open",
    className: "kpi-card-open",
  },
  {
    key: "resolved",
    label: "Resolved",
    className: "kpi-card-resolved",
  },
  {
    key: "escalations",
    label: "Escalations Required",
    className: "kpi-card-escalations",
  },
];

function calculateKpis(incidents) {
  return {
    total: incidents.length,
    critical: incidents.filter((incident) => incident.severity === "critical")
      .length,
    high: incidents.filter((incident) => incident.severity === "high").length,
    open: incidents.filter((incident) => incident.status === "open").length,
    resolved: incidents.filter((incident) => incident.status === "resolved")
      .length,
    escalations: incidents.filter((incident) => incident.requires_escalation)
      .length,
  };
}

export default function OverviewDashboard({ refreshKey }) {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadIncidents() {
      try {
        setLoading(true);
        setError("");
        const data = await getIncidents();
        setIncidents(data);
      } catch (requestError) {
        setError(
          "Could not load overview analytics. Make sure the backend server is running."
        );
      } finally {
        setLoading(false);
      }
    }

    loadIncidents();
  }, [refreshKey]);

  if (loading) {
    return <p className="table-message">Loading overview metrics...</p>;
  }

  if (error) {
    return <p className="table-message table-error">{error}</p>;
  }

  if (incidents.length === 0) {
    return <p className="table-message">No incidents available yet.</p>;
  }

  const kpis = calculateKpis(incidents);

  return (
    <section className="content-stack">
      <article className="panel">
        <h2>Overview</h2>
        <p>
          Monitor current incident volume, severity distribution, and
          escalation needs across the AI Ops workflow.
        </p>

        <div className="kpi-grid">
          {kpiCards.map((card) => (
            <div key={card.key} className={`kpi-card ${card.className}`}>
              <span className="kpi-label">{card.label}</span>
              <strong className="kpi-value">{kpis[card.key]}</strong>
            </div>
          ))}
        </div>
      </article>
    </section>
  );
}
