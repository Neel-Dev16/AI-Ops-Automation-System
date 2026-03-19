from datetime import datetime

from pydantic import BaseModel


class IncidentCreate(BaseModel):
    service_name: str
    severity: str
    incident_type: str
    raw_logs: str | None = None
    summary: str
    root_cause: str
    recommended_actions: str
    requires_escalation: bool
    escalation_message: str | None = None
    automation_action: str | None = None
    priority_score: int | None = None
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
    escalation_message: str | None = None
    automation_action: str | None = None
    priority_score: int | None = None


class IncidentStatusUpdate(BaseModel):
    status: str


class IncidentResponse(BaseModel):
    id: int
    service_name: str
    severity: str
    incident_type: str
    raw_logs: str | None = None
    summary: str
    root_cause: str
    recommended_actions: str
    requires_escalation: bool
    escalation_message: str | None = None
    automation_action: str | None = None
    priority_score: int | None = None
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class ServiceResponse(BaseModel):
    id: int
    name: str
    environment: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class RawLogCreate(BaseModel):
    service_name: str
    environment: str = "development"
    level: str
    message: str
    raw_payload: str | None = None
    source: str | None = None


class RawLogResponse(BaseModel):
    id: int
    service_name: str
    environment: str
    level: str
    message: str
    raw_payload: str | None = None
    source: str | None = None
    processed: bool
    triage_decision: str | None = None
    risk_score: int | None = None
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
