from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Incident
from app.schemas import IncidentCreate, IncidentResponse, IncidentStatusUpdate


router = APIRouter()
VALID_INCIDENT_STATUSES = {"open", "investigating", "resolved", "ignored"}


def get_incident_or_404(incident_id: int, db: Session) -> Incident:
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.get("/", response_model=list[IncidentResponse])
def list_incidents(db: Session = Depends(get_db)) -> list[Incident]:
    return db.query(Incident).order_by(Incident.created_at.desc()).all()


@router.post("/test", response_model=IncidentResponse, status_code=201)
def create_test_incident(db: Session = Depends(get_db)) -> Incident:
    payload = IncidentCreate(
        service_name="payment-service",
        severity="high",
        incident_type="database_timeout",
        raw_logs="ERROR payment-service database timeout after 30s. Connection pool exhausted.",
        summary="Database connection timeout detected",
        root_cause="Connection pool exhaustion",
        recommended_actions="Check DB pool, inspect slow queries",
        requires_escalation=True,
    )

    incident = Incident(**payload.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db)) -> Incident:
    return get_incident_or_404(incident_id, db)


@router.patch("/{incident_id}/status", response_model=IncidentResponse)
def update_incident_status(
    incident_id: int,
    payload: IncidentStatusUpdate,
    db: Session = Depends(get_db),
) -> Incident:
    if payload.status not in VALID_INCIDENT_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Invalid status. Valid statuses are: open, investigating, resolved, ignored",
        )

    incident = get_incident_or_404(incident_id, db)
    incident.status = payload.status
    db.commit()
    db.refresh(incident)
    return incident
