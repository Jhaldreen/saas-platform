from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum, Text, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from ..database import Base

class RuleSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Rule(Base):
    __tablename__ = 'rules'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=False, index=True)
    
    # Rule definition
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    audit_type = Column(String, nullable=False, index=True)  # cloud, hospitality, business
    
    # Rule logic (stored as JSON)
    # Example: {"field": "cost", "operator": ">", "threshold": 1000}
    conditions = Column(JSON, nullable=False)
    
    severity = Column(SQLEnum(RuleSeverity), default=RuleSeverity.MEDIUM, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="rules")
    findings = relationship("Finding", back_populates="rule")
