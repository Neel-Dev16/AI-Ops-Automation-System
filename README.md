# AI Ops Automation System

## Motivation

Modern systems generate large volumes of logs and events. This project is intended to help teams turn that raw operational data into structured incident analysis, faster root-cause discovery, and actionable remediation guidance.

## Planned Features

- Log and event ingestion for multiple application services
- LLM-assisted incident analysis with structured summaries
- Severity classification and remediation recommendations
- Validation against sample incident ground truth
- Dockerized local development for backend and frontend services

## Prerequisites

- Python 3.11+
- Node.js 20+
- npm
- Docker Desktop or Docker Engine

## Run Backend Locally

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

## Run Frontend Locally

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

- App: [http://localhost:5173](http://localhost:5173)

Note: Vite may automatically move to `5174` or `5175` if `5173` is already in use.

## Run Full App With Docker Compose

From the project root:

```bash
docker compose up --build
```

Expected URLs:

- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend: [http://127.0.0.1:8000](http://127.0.0.1:8000)

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
