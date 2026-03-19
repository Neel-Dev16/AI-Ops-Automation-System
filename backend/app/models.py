from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    environment = Column(String, nullable=False, default="development")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class RawLog(Base):
    __tablename__ = "raw_logs"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, index=True, nullable=False)
    environment = Column(String, nullable=False, default="development")
    level = Column(String, index=True, nullable=False)
    message = Column(Text, nullable=False)
    raw_payload = Column(Text, nullable=True)
    source = Column(String, nullable=True)
    processed = Column(Boolean, nullable=False, default=False)
    triage_decision = Column(String, nullable=True)
    risk_score = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


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
