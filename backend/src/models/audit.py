from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from ..database import Base

class AuditType(str, enum.Enum):
    CLOUD = "cloud"
    HOSPITALITY = "hospitality"
    BUSINESS = "business"

class AuditStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Audit(Base):
    __tablename__ = 'audits'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=False, index=True)
    audit_type = Column(SQLEnum(AuditType), nullable=False, index=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    
    # Metrics
    total_cost_or_revenue = Column(Float, nullable=True)
    optimization_score = Column(Integer, nullable=True)  # 0-100
    
    # Status
    status = Column(SQLEnum(AuditStatus), default=AuditStatus.PENDING, nullable=False)
    error_message = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="audits")
    created_by_user = relationship("User", back_populates="audits")
    findings = relationship("Finding", back_populates="audit", cascade="all, delete-orphan")
