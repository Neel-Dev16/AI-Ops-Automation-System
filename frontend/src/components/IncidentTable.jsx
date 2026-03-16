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
  const [selectedIncident, setSelectedIncident] = useState(null);
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
      setSelectedIncident((currentIncident) => {
        if (!currentIncident) {
          return null;
        }

        return (
          data.find((incident) => incident.id === currentIncident.id) || null
        );
      });
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
      const updatedIncident = await updateIncidentStatus(incidentId, status);

      setIncidents((currentIncidents) =>
        currentIncidents.map((incident) =>
          incident.id === updatedIncident.id ? updatedIncident : incident
        )
      );
      setSelectedIncident((currentIncident) =>
        currentIncident?.id === updatedIncident.id
          ? updatedIncident
          : currentIncident
      );
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
    <div className="incident-history-layout">
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
              <tr
                key={incident.id}
                className={
                  selectedIncident?.id === incident.id
                    ? "incident-row incident-row-selected"
                    : "incident-row"
                }
                onClick={() => setSelectedIncident(incident)}
              >
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
                      onClick={(event) => {
                        event.stopPropagation();
                        handleStatusUpdate(incident.id, "investigating");
                      }}
                      disabled={updatingId === incident.id}
                    >
                      {updatingId === incident.id
                        ? "Updating..."
                        : "Investigating"}
                    </button>
                    <button
                      type="button"
                      className="status-button"
                      onClick={(event) => {
                        event.stopPropagation();
                        handleStatusUpdate(incident.id, "resolved");
                      }}
                      disabled={updatingId === incident.id}
                    >
                      Resolved
                    </button>
                    <button
                      type="button"
                      className="status-button"
                      onClick={(event) => {
                        event.stopPropagation();
                        handleStatusUpdate(incident.id, "ignored");
                      }}
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

      <aside className="incident-detail-panel">
        {selectedIncident ? (
          <>
            <div className="detail-header">
              <h3>Incident Details</h3>
              <span className={severityClassName(selectedIncident.severity)}>
                {selectedIncident.severity}
              </span>
            </div>

            <dl className="detail-grid">
              <div>
                <dt>ID</dt>
                <dd>{selectedIncident.id}</dd>
              </div>
              <div>
                <dt>Service</dt>
                <dd>{selectedIncident.service_name}</dd>
              </div>
              <div>
                <dt>Incident Type</dt>
                <dd>{selectedIncident.incident_type}</dd>
              </div>
              <div>
                <dt>Status</dt>
                <dd>{selectedIncident.status}</dd>
              </div>
              <div>
                <dt>Priority Score</dt>
                <dd>{selectedIncident.priority_score ?? "N/A"}</dd>
              </div>
              <div>
                <dt>Escalation Required</dt>
                <dd>{selectedIncident.requires_escalation ? "Yes" : "No"}</dd>
              </div>
              <div>
                <dt>Created At</dt>
                <dd>{formatDate(selectedIncident.created_at)}</dd>
              </div>
              <div>
                <dt>Automation Action</dt>
                <dd>{selectedIncident.automation_action || "N/A"}</dd>
              </div>
            </dl>

            <div className="detail-section">
              <h4>Summary</h4>
              <p>{selectedIncident.summary || "N/A"}</p>
            </div>

            <div className="detail-section">
              <h4>Root Cause</h4>
              <p>{selectedIncident.root_cause || "N/A"}</p>
            </div>

            <div className="detail-section">
              <h4>Recommended Actions</h4>
              <p>{selectedIncident.recommended_actions || "N/A"}</p>
            </div>

            <div className="detail-section">
              <h4>Escalation Message</h4>
              <p>{selectedIncident.escalation_message || "N/A"}</p>
            </div>

            <div className="detail-section">
              <h4>Raw Logs</h4>
              <pre className="raw-logs-block">
                {selectedIncident.raw_logs || "No raw logs stored for this incident."}
              </pre>
            </div>
          </>
        ) : (
          <div className="detail-placeholder">
            <h3>Incident Details</h3>
            <p>
              Select an incident from the table to review its full context,
              automation metadata, and original raw logs.
            </p>
          </div>
        )}
      </aside>
    </div>
  );
}
