# AI Ops Automation System

## What Problem It Solves

Modern systems produce large amounts of operational noise. This project demonstrates how an AIOps platform can turn raw logs into structured incidents with triage, redaction, grouping, severity classification, root-cause summaries, and remediation guidance.

It is designed as a portfolio-friendly, demo-ready full-stack system that shows both manual and automated log workflows.

## Features

- manual log analysis from the frontend
- raw log ingestion APIs for multiple services
- rule-based triage before analysis
- sensitive data redaction before LLM processing
- mock and OpenAI-backed incident analysis modes
- incident automation metadata such as priority and escalation actions
- fingerprint-based grouping for repeated issues
- raw log retention pruning
- live dashboard views for incidents and raw logs
- optional simulated log producer for demos
- Docker Compose support for local full-stack runs

## Architecture

The system consists of:

- React dashboard frontend
- FastAPI backend
- SQLite persistence layer
- raw log ingestion and incident APIs
- triage, redaction, fingerprinting, automation, and retention services
- optional simulated log producer

Architecture details and diagrams are available in [docs/architecture.md](/Users/neel/Documents/New project/AIops/AI-Ops-Automation-System/docs/architecture.md).

## Screenshots

Screenshot placeholders:

- Overview dashboard
- Incident History detail panel
- Raw Logs page
- Analyze Logs page

## Prerequisites

- Python 3.11+
- Node.js 20+
- npm
- Docker Desktop or Docker Engine

## Setup

### Run Backend Locally

From the project root:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend URL:

- API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Health check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### Run Frontend Locally

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

- App: [http://localhost:5173](http://localhost:5173)

Note: Vite may automatically move to `5174` or `5175` if `5173` is already in use.

## Demo Commands

### Full stack without simulated logs

From the project root:

```bash
docker compose up --build
```

### Full stack with simulated logs

```bash
docker compose --profile producer up --build
```

Expected URLs:

- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## API Examples

### Analyze logs manually

```bash
curl -X POST http://127.0.0.1:8000/api/logs/analyze \
  -H "Content-Type: application/json" \
  -d '{"raw_logs":"ERROR payment-service database timeout after 30s. Connection pool exhausted."}'
```

### Ingest a raw log

```bash
curl -X POST http://127.0.0.1:8000/api/logs/ingest \
  -H "Content-Type: application/json" \
  -d '{"service_name":"payment-service","environment":"production","level":"ERROR","message":"Database timeout after 30s","source":"payment-api"}'
```

### Fetch raw logs

```bash
curl http://127.0.0.1:8000/api/logs/raw
```

### Fetch incidents

```bash
curl http://127.0.0.1:8000/api/incidents/
```

## Validation

Run the mock analysis validator:

```bash
python3 scripts/validate_analysis.py
```

Run the simulated log producer locally:

```bash
python3 scripts/log_producer.py
```

## Future Improvements

- replace SQLite with PostgreSQL for more realistic persistence
- add database migrations with Alembic
- add authentication and role-based access for maintenance endpoints
- add background workers for asynchronous ingestion and analysis
- add richer grouping logic across services and time windows
- add alert integrations such as Slack, email, or PagerDuty
- add charts for historical trend analysis and service health scoring

## Troubleshooting

- Port already in use:
  Stop the process already using `8000` or `5173`, or close old dev servers and containers before restarting.
- Backend not reachable:
  Make sure the backend is running on `http://127.0.0.1:8000` and confirm with:

  ```bash
  curl http://127.0.0.1:8000/health
  ```

- SQLite schema changed:
  If the local database schema is out of date, stop the backend and delete the local SQLite file:

  ```bash
  rm backend/aiops.db
  ```

  Then restart the backend so FastAPI recreates the table.
