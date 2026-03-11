import React, { useEffect, useState } from "react";

import { getIncidents, updateIncidentStatus } from "../api/incidents";

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

export default function IncidentTable({ refreshKey }) {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [updatingId, setUpdatingId] = useState(null);
  const [updateError, setUpdateError] = useState("");

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

  useEffect(() => {
    loadIncidents();
  }, [refreshKey]);

  async function handleStatusUpdate(incidentId, status) {
    try {
      setUpdatingId(incidentId);
      setUpdateError("");
      await updateIncidentStatus(incidentId, status);
      await loadIncidents();
    } catch (requestError) {
      setUpdateError("Could not update incident status. Please try again.");
    } finally {
      setUpdatingId(null);
    }
  }

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
      {updateError ? (
        <p className="table-message table-error">{updateError}</p>
      ) : null}

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
            <th>Actions</th>
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
              <td>
                <div className="status-actions">
                  <button
                    type="button"
                    className="status-button"
                    onClick={() =>
                      handleStatusUpdate(incident.id, "investigating")
                    }
                    disabled={updatingId === incident.id}
                  >
                    {updatingId === incident.id ? "Updating..." : "Investigating"}
                  </button>
                  <button
                    type="button"
                    className="status-button"
                    onClick={() => handleStatusUpdate(incident.id, "resolved")}
                    disabled={updatingId === incident.id}
                  >
                    Resolved
                  </button>
                  <button
                    type="button"
                    className="status-button"
                    onClick={() => handleStatusUpdate(incident.id, "ignored")}
                    disabled={updatingId === incident.id}
                  >
                    Ignored
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
