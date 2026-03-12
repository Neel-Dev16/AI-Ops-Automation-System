# Demo Guide

## Prerequisites

- Python 3.11+
- Node.js 20+
- npm
- Docker Desktop or Docker Engine

## Local Demo Flow

### 1. Start the backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend URL:

- [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 2. Start the frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

- [http://localhost:5173](http://localhost:5173)

### 3. Use the app

- Open the frontend
- Review incidents in the dashboard table
- Paste logs into the Analyze Logs form
- Submit logs to create a new incident
- Update incident status from the dashboard

## Docker Compose Demo

From the project root:

```bash
docker compose up --build
```

URLs:

- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Troubleshooting

- Port already in use:
  Stop any process or container already using `8000` or `5173`.
- Backend not reachable:
  Check the backend with:

  ```bash
  curl http://127.0.0.1:8000/health
  ```

- Local SQLite database problems after schema changes:

  ```bash
  rm backend/aiops.db
  ```

  Restart the backend after deleting it so a fresh database is created.
