# API Contract

This document summarizes the current backend endpoints for the AI Ops Automation System.

## GET /health

Purpose: Check whether the backend service is running.

Response example:

```json
{
  "status": "ok",
  "service": "ai-ops-backend"
}
```

curl command:

```bash
curl http://127.0.0.1:8000/health
```

## GET /api/incidents

Purpose: Return all stored incidents, newest first.

Response example:

```json
[
  {
    "id": 6,
    "service_name": "payment-service",
    "severity": "high",
    "incident_type": "database_timeout",
    "summary": "Database timeout or connection pool issue detected in the logs.",
    "root_cause": "Database connection pool exhaustion or timeout",
    "recommended_actions": "Check database pool settings, inspect slow queries, and review database availability.",
    "requires_escalation": true,
    "escalation_message": "High-severity incident detected. Escalate to the engineering team for urgent investigation.",
    "automation_action": "escalate_to_engineering",
    "priority_score": 80,
    "status": "open",
    "created_at": "2026-04-29T03:58:58.765209"
  }
]
```

curl command:

```bash
curl http://127.0.0.1:8000/api/incidents/
```

## GET /api/incidents/{incident_id}

Purpose: Return one incident by its ID.

Response example:

```json
{
  "id": 6,
  "service_name": "payment-service",
  "severity": "high",
  "incident_type": "database_timeout",
  "summary": "Database timeout or connection pool issue detected in the logs.",
  "root_cause": "Database connection pool exhaustion or timeout",
  "recommended_actions": "Check database pool settings, inspect slow queries, and review database availability.",
  "requires_escalation": true,
  "escalation_message": "High-severity incident detected. Escalate to the engineering team for urgent investigation.",
  "automation_action": "escalate_to_engineering",
  "priority_score": 80,
  "status": "open",
  "created_at": "2026-04-29T03:58:58.765209"
}
```

curl command:

```bash
curl http://127.0.0.1:8000/api/incidents/6
```

## POST /api/incidents/test

Purpose: Create a dummy incident for testing the incident storage flow.

Response example:

```json
{
  "id": 7,
  "service_name": "payment-service",
  "severity": "high",
  "incident_type": "database_timeout",
  "summary": "Database connection timeout detected",
  "root_cause": "Connection pool exhaustion",
  "recommended_actions": "Check DB pool, inspect slow queries",
  "requires_escalation": true,
  "escalation_message": null,
  "automation_action": null,
  "priority_score": null,
  "status": "open",
  "created_at": "2026-04-29T04:10:00.000000"
}
```

curl command:

```bash
curl -X POST http://127.0.0.1:8000/api/incidents/test
```

## POST /api/logs/analyze

Purpose: Analyze raw logs with the mock LLM service, apply automation rules, save the generated incident, and return it.

Request example:

```json
{
  "raw_logs": "ERROR payment-service database timeout after 30s. Connection pool exhausted."
}
```

Response example:

```json
{
  "id": 8,
  "service_name": "payment-service",
  "severity": "high",
  "incident_type": "database_timeout",
  "summary": "Database timeout or connection pool issue detected in the logs.",
  "root_cause": "Database connection pool exhaustion or timeout",
  "recommended_actions": "Check database pool settings, inspect slow queries, and review database availability.",
  "requires_escalation": true,
  "escalation_message": "High-severity incident detected. Escalate to the engineering team for urgent investigation.",
  "automation_action": "escalate_to_engineering",
  "priority_score": 80,
  "status": "open",
  "created_at": "2026-04-29T04:12:00.000000"
}
```

curl command:

```bash
curl -X POST http://127.0.0.1:8000/api/logs/analyze \
  -H "Content-Type: application/json" \
  -d '{"raw_logs":"ERROR payment-service database timeout after 30s. Connection pool exhausted."}'
```

## PATCH /api/incidents/{incident_id}/status

Purpose: Update the status of an incident.

Valid statuses:
- `open`
- `investigating`
- `resolved`
- `ignored`

Request example:

```json
{
  "status": "resolved"
}
```

Response example:

```json
{
  "id": 6,
  "service_name": "payment-service",
  "severity": "high",
  "incident_type": "database_timeout",
  "summary": "Database timeout or connection pool issue detected in the logs.",
  "root_cause": "Database connection pool exhaustion or timeout",
  "recommended_actions": "Check database pool settings, inspect slow queries, and review database availability.",
  "requires_escalation": true,
  "escalation_message": "High-severity incident detected. Escalate to the engineering team for urgent investigation.",
  "automation_action": "escalate_to_engineering",
  "priority_score": 80,
  "status": "resolved",
  "created_at": "2026-04-29T03:58:58.765209"
}
```

curl command:

```bash
curl -X PATCH http://127.0.0.1:8000/api/incidents/6/status \
  -H "Content-Type: application/json" \
  -d '{"status":"resolved"}'
```
