from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    incident_type = Column(String, nullable=False)
    raw_logs = Column(Text, nullable=True)
    summary = Column(String, nullable=False)
    root_cause = Column(Text, nullable=False)
    recommended_actions = Column(Text, nullable=False)
    requires_escalation = Column(Boolean, nullable=False, default=False)
    escalation_message = Column(Text, nullable=True)
    automation_action = Column(String, nullable=True)
    priority_score = Column(Integer, nullable=True)
    status = Column(String, nullable=False, default="open")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
