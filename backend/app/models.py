from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    incident_type = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    root_cause = Column(Text, nullable=False)
    recommended_actions = Column(Text, nullable=False)
    requires_escalation = Column(Boolean, nullable=False, default=False)
    status = Column(String, nullable=False, default="open")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
