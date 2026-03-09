from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.database import Base, engine
from app.routers.health import router as health_router
from app.routers.incidents import router as incidents_router
from app.routers.logs import router as logs_router


ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
]


app = FastAPI(
    title="AI Ops Automation System",
    description="Backend API for ingesting logs and automating incident analysis.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    # Importing models ensures SQLAlchemy knows about the Incident table.
    Base.metadata.create_all(bind=engine)


app.include_router(health_router)
app.include_router(logs_router, prefix="/api/logs", tags=["logs"])
app.include_router(incidents_router, prefix="/api/incidents", tags=["incidents"])


@app.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    return {
        "message": "AI Ops Automation System backend is running.",
    }
