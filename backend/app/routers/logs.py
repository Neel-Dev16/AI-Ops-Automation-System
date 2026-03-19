from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Incident, RawLog, Service
from app.schemas import (
    IncidentCreate,
    IncidentResponse,
    LogAnalysisRequest,
    RawLogCreate,
    RawLogResponse,
)
from app.services.automation_service import apply_automation_rules
from app.services.llm_service import analyze_logs_with_llm

router = APIRouter()


def get_or_create_service(db: Session, service_name: str, environment: str) -> Service:
    service = (
        db.query(Service)
        .filter(Service.name == service_name, Service.environment == environment)
        .first()
    )
    if service is not None:
        return service

    service = Service(name=service_name, environment=environment)
    db.add(service)
    db.flush()
    return service


@router.get("/")
def list_logs() -> dict[str, str]:
    return {"message": "Logs endpoint placeholder."}


@router.post("/ingest", response_model=RawLogResponse, status_code=201)
def ingest_log(payload: RawLogCreate, db: Session = Depends(get_db)) -> RawLog:
    get_or_create_service(db, payload.service_name, payload.environment)

    raw_log = RawLog(**payload.model_dump())
    db.add(raw_log)
    db.commit()
    db.refresh(raw_log)
    return raw_log


@router.post("/batch", response_model=list[RawLogResponse], status_code=201)
def ingest_logs_batch(
    payload: list[RawLogCreate], db: Session = Depends(get_db)
) -> list[RawLog]:
    raw_logs: list[RawLog] = []

    for item in payload:
        get_or_create_service(db, item.service_name, item.environment)
        raw_log = RawLog(**item.model_dump())
        db.add(raw_log)
        raw_logs.append(raw_log)

    db.commit()

    for raw_log in raw_logs:
        db.refresh(raw_log)

    return raw_logs


@router.get("/raw", response_model=list[RawLogResponse])
def list_raw_logs(
    service_name: str | None = None,
    level: str | None = None,
    processed: bool | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[RawLog]:
    query = db.query(RawLog)

    if service_name:
        query = query.filter(RawLog.service_name == service_name)

    if level:
        query = query.filter(RawLog.level == level)

    if processed is not None:
        query = query.filter(RawLog.processed == processed)

    return query.order_by(RawLog.created_at.desc()).limit(limit).all()


@router.post("/analyze", response_model=IncidentResponse, status_code=201)
def analyze_logs(payload: LogAnalysisRequest, db: Session = Depends(get_db)) -> Incident:
    analysis = analyze_logs_with_llm(payload.raw_logs)
    automation_metadata = apply_automation_rules(analysis)
    analysis_data = analysis.model_dump()

    for key in ("escalation_message", "automation_action", "priority_score"):
        analysis_data.pop(key, None)

    incident_data = IncidentCreate(
        **analysis_data,
        raw_logs=payload.raw_logs,
        **automation_metadata,
    )

    incident = Incident(**incident_data.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident
