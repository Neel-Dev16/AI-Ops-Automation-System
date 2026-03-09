import apiClient from "./client";

export async function getIncidents() {
  const response = await apiClient.get("/api/incidents/");
  return response.data;
}

export async function analyzeLogs(rawLogs) {
  const response = await apiClient.post("/api/logs/analyze", {
    raw_logs: rawLogs,
  });
  return response.data;
}

export async function updateIncidentStatus(id, status) {
  const response = await apiClient.patch(`/api/incidents/${id}/status`, {
    status,
  });
  return response.data;
}
