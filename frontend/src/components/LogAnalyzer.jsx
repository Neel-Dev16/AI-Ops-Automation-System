import React, { useState } from "react";

import { analyzeLogs } from "../api/incidents";

const SAMPLE_LOG = `ERROR payment-service database timeout after 30s.
Connection pool exhausted.
Retry attempts failed.`;

export default function LogAnalyzer({ onAnalysisComplete }) {
  const [rawLogs, setRawLogs] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze(event) {
    event.preventDefault();

    if (!rawLogs.trim()) {
      setError("Please paste some logs before running analysis.");
      setResult(null);
      return;
    }

    try {
      setLoading(true);
      setError("");
      const incident = await analyzeLogs(rawLogs);
      setResult(incident);
      onAnalysisComplete?.();
    } catch (requestError) {
      setError(
        "Analysis failed. Make sure the backend server is running and accessible."
      );
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  function handleUseSampleLog() {
    setRawLogs(SAMPLE_LOG);
    setError("");
  }

  return (
    <div className="log-analyzer">
      <form className="log-form" onSubmit={handleAnalyze}>
        <label className="log-label" htmlFor="raw-logs">
          Raw Logs
        </label>
        <textarea
          id="raw-logs"
          className="log-textarea"
          value={rawLogs}
          onChange={(event) => setRawLogs(event.target.value)}
          placeholder="Paste raw application logs here..."
          rows={8}
        />

        <div className="log-actions">
          <button
            type="button"
            className="secondary-button"
            onClick={handleUseSampleLog}
          >
            Use Sample Log
          </button>
          <button type="submit" className="primary-button" disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Logs"}
          </button>
        </div>
      </form>

      {error ? <p className="table-message table-error">{error}</p> : null}

      {result ? (
        <div className="analysis-result">
          <h3>Analyzed Incident</h3>
          <dl className="result-grid">
            <div>
              <dt>Service</dt>
              <dd>{result.service_name}</dd>
            </div>
            <div>
              <dt>Severity</dt>
              <dd>{result.severity}</dd>
            </div>
            <div>
              <dt>Incident Type</dt>
              <dd>{result.incident_type}</dd>
            </div>
            <div>
              <dt>Summary</dt>
              <dd>{result.summary}</dd>
            </div>
            <div>
              <dt>Root Cause</dt>
              <dd>{result.root_cause}</dd>
            </div>
            <div>
              <dt>Recommended Actions</dt>
              <dd>{result.recommended_actions}</dd>
            </div>
            <div>
              <dt>Escalation Required</dt>
              <dd>{result.requires_escalation ? "Yes" : "No"}</dd>
            </div>
            <div>
              <dt>Priority Score</dt>
              <dd>{result.priority_score ?? "N/A"}</dd>
            </div>
            <div>
              <dt>Automation Action</dt>
              <dd>{result.automation_action ?? "N/A"}</dd>
            </div>
            <div>
              <dt>Escalation Message</dt>
              <dd>{result.escalation_message ?? "N/A"}</dd>
            </div>
          </dl>
        </div>
      ) : null}
    </div>
  );
}
