import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

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

const severityColors = {
  critical: "#d64545",
  high: "#eb8a2f",
  medium: "#d4ad21",
  low: "#2e8b57",
  unknown: "#7a8da6",
};

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

function buildSeverityData(incidents) {
  const counts = {
    critical: 0,
    high: 0,
    medium: 0,
    low: 0,
  };

  incidents.forEach((incident) => {
    const key = incident.severity?.toLowerCase();
    if (counts[key] !== undefined) {
      counts[key] += 1;
    }
  });

  return Object.entries(counts)
    .filter(([, value]) => value > 0)
    .map(([name, value]) => ({
      name,
      value,
      color: severityColors[name] || severityColors.unknown,
    }));
}

function buildTrendData(incidents) {
  const countsByDay = {};

  incidents.forEach((incident) => {
    const createdAt = incident.created_at ? new Date(incident.created_at) : null;
    if (!createdAt || Number.isNaN(createdAt.getTime())) {
      return;
    }

    const label = createdAt.toLocaleDateString(undefined, {
      month: "short",
      day: "numeric",
    });

    countsByDay[label] = (countsByDay[label] || 0) + 1;
  });

  return Object.entries(countsByDay).map(([date, incidentsCount]) => ({
    date,
    incidents: incidentsCount,
  }));
}

function formatFeedTime(value) {
  if (!value) {
    return "Unknown time";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "Unknown time";
  }

  return date.toLocaleString();
}

function severityClassName(severity) {
  return `severity-badge severity-${severity?.toLowerCase() || "unknown"}`;
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
  const severityData = buildSeverityData(incidents);
  const trendData = buildTrendData(incidents);
  const recentIncidents = [...incidents].slice(0, 5);

  return (
    <section className="content-stack">
      <article className="panel">
        <h2>Overview</h2>
        <p>
          Monitor current incident volume, severity distribution, and
          escalation needs across the AI Ops workflow.
        </p>

        <div className="kpi-grid">
          {kpiCards.map((card, index) => (
            <motion.div
              key={card.key}
              className={`kpi-card ${card.className}`}
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.35, delay: index * 0.08 }}
            >
              <span className="kpi-label">{card.label}</span>
              <strong className="kpi-value">{kpis[card.key]}</strong>
            </motion.div>
          ))}
        </div>
      </article>

      <section className="overview-grid">
        <article className="panel">
          <h3>Severity Distribution</h3>
          <p>Current incident mix by severity level.</p>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={severityData}
                  dataKey="value"
                  nameKey="name"
                  innerRadius={65}
                  outerRadius={100}
                  paddingAngle={4}
                  isAnimationActive
                >
                  {severityData.map((entry) => (
                    <Cell key={entry.name} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-legend">
            {severityData.map((entry) => (
              <div key={entry.name} className="legend-item">
                <span
                  className="legend-swatch"
                  style={{ backgroundColor: entry.color }}
                />
                <span className="legend-label">
                  {entry.name}: {entry.value}
                </span>
              </div>
            ))}
          </div>
        </article>

        <article className="panel">
          <h3>Incident Trend</h3>
          <p>Recent incident creation trend based on stored timestamps.</p>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={trendData}>
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="incidents"
                  stroke="#1d4ed8"
                  strokeWidth={3}
                  dot={{ r: 4, fill: "#1d4ed8" }}
                  activeDot={{ r: 6 }}
                  isAnimationActive
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </article>
      </section>

      <article className="panel">
        <h3>Live Incident Feed</h3>
        <p>The five most recent incidents saved by the backend analysis flow.</p>

        <div className="feed-list">
          {recentIncidents.map((incident) => (
            <div key={incident.id} className="feed-item">
              <div className="feed-item-main">
                <span className={severityClassName(incident.severity)}>
                  {incident.severity}
                </span>
                <div className="feed-text">
                  <strong>{incident.service_name}</strong>
                  <span>{incident.incident_type}</span>
                </div>
              </div>

              <div className="feed-meta">
                <span className="feed-status">{incident.status}</span>
                <span className="feed-time">
                  {formatFeedTime(incident.created_at)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </article>
    </section>
  );
}
