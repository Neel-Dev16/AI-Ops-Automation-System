from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Incident
from app.schemas import IncidentCreate, IncidentResponse, LogAnalysisRequest
from app.services.llm_service import analyze_logs_with_llm

router = APIRouter()


@router.get("/")
def list_logs() -> dict[str, str]:
    return {"message": "Logs endpoint placeholder."}


@router.post("/analyze", response_model=IncidentResponse, status_code=201)
def analyze_logs(payload: LogAnalysisRequest, db: Session = Depends(get_db)) -> Incident:
    analysis = analyze_logs_with_llm(payload.raw_logs)

    incident_data = IncidentCreate(
        service_name=analysis.service_name,
        severity=analysis.severity,
        incident_type=analysis.incident_type,
        summary=analysis.summary,
        root_cause=analysis.root_cause,
        recommended_actions=analysis.recommended_actions,
        requires_escalation=analysis.requires_escalation,
    )

    incident = Incident(**incident_data.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident
