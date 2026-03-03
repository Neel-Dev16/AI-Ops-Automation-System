from datetime import datetime

from pydantic import BaseModel


class IncidentCreate(BaseModel):
    service_name: str
    severity: str
    incident_type: str
    summary: str
    root_cause: str
    recommended_actions: str
    requires_escalation: bool
    status: str = "open"


class LogAnalysisRequest(BaseModel):
    raw_logs: str


class IncidentAnalysisResult(BaseModel):
    service_name: str
    severity: str
    incident_type: str
    summary: str
    root_cause: str
    recommended_actions: str
    requires_escalation: bool


class IncidentResponse(BaseModel):
    id: int
    service_name: str
    severity: str
    incident_type: str
    summary: str
    root_cause: str
    recommended_actions: str
    requires_escalation: bool
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
