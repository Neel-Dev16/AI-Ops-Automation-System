import React, { useEffect, useState } from "react";

import { getIncidents } from "../api/incidents";

function formatDate(value) {
  if (!value) {
    return "N/A";
  }

  const date = new Date(value);
  return date.toLocaleString();
}

function severityClassName(severity) {
  return `severity-badge severity-${severity?.toLowerCase() || "unknown"}`;
}

export default function IncidentTable() {
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
          "Could not load incidents. Make sure the backend server is running."
        );
      } finally {
        setLoading(false);
      }
    }

    loadIncidents();
  }, []);

  if (loading) {
    return <p className="table-message">Loading incidents...</p>;
  }

  if (error) {
    return <p className="table-message table-error">{error}</p>;
  }

  if (incidents.length === 0) {
    return <p className="table-message">No incidents found yet.</p>;
  }

  return (
    <div className="table-wrapper">
      <table className="incident-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Service</th>
            <th>Severity</th>
            <th>Incident Type</th>
            <th>Status</th>
            <th>Priority Score</th>
            <th>Escalation Required</th>
            <th>Created At</th>
          </tr>
        </thead>
        <tbody>
          {incidents.map((incident) => (
            <tr key={incident.id}>
              <td>{incident.id}</td>
              <td>{incident.service_name}</td>
              <td>
                <span className={severityClassName(incident.severity)}>
                  {incident.severity}
                </span>
              </td>
              <td>{incident.incident_type}</td>
              <td>{incident.status}</td>
              <td>{incident.priority_score ?? "N/A"}</td>
              <td>{incident.requires_escalation ? "Yes" : "No"}</td>
              <td>{formatDate(incident.created_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
