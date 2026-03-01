from fastapi import FastAPI

from app.routers.health import router as health_router
from app.routers.incidents import router as incidents_router
from app.routers.logs import router as logs_router


app = FastAPI(
    title="AI Ops Automation System",
    description="Backend API for ingesting logs and automating incident analysis.",
    version="0.1.0",
)


app.include_router(health_router)
app.include_router(logs_router, prefix="/logs", tags=["logs"])
app.include_router(incidents_router, prefix="/incidents", tags=["incidents"])


@app.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    return {
        "message": "AI Ops Automation System backend is running.",
    }
