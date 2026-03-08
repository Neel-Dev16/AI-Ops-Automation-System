from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Incident
from app.schemas import IncidentCreate, IncidentResponse, LogAnalysisRequest
from app.services.automation_service import apply_automation_rules
from app.services.llm_service import analyze_logs_with_llm

router = APIRouter()


@router.get("/")
def list_logs() -> dict[str, str]:
    return {"message": "Logs endpoint placeholder."}


@router.post("/analyze", response_model=IncidentResponse, status_code=201)
def analyze_logs(payload: LogAnalysisRequest, db: Session = Depends(get_db)) -> Incident:
    analysis = analyze_logs_with_llm(payload.raw_logs)
    automation_metadata = apply_automation_rules(analysis)
    analysis_data = analysis.model_dump()

    for key in ("escalation_message", "automation_action", "priority_score"):
        analysis_data.pop(key, None)

    incident_data = IncidentCreate(
        **analysis_data,
        **automation_metadata,
    )

    incident = Incident(**incident_data.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident
