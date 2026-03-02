from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Incident
from app.schemas import IncidentCreate, IncidentResponse


router = APIRouter()


@router.get("/", response_model=list[IncidentResponse])
def list_incidents(db: Session = Depends(get_db)) -> list[Incident]:
    return db.query(Incident).order_by(Incident.created_at.desc()).all()


@router.post("/test", response_model=IncidentResponse, status_code=201)
def create_test_incident(db: Session = Depends(get_db)) -> Incident:
    payload = IncidentCreate(
        service_name="payment-service",
        severity="high",
        incident_type="database_timeout",
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
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident
