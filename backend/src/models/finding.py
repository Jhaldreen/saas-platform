from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..database import Base

class Finding(Base):
    __tablename__ = 'findings'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    audit_id = Column(UUID(as_uuid=True), ForeignKey('audits.id'), nullable=False, index=True)
    rule_id = Column(UUID(as_uuid=True), ForeignKey('rules.id'), nullable=True, index=True)
    
    # Finding details
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String, nullable=False)  # Inherited from rule
    
    # Impact
    cost_impact = Column(Float, nullable=True)  # Potential savings or loss
    
    # Evidence (CSV row data that triggered the rule)
    evidence = Column(JSON, nullable=True)
    
    # Recommendations
    recommendation = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    audit = relationship("Audit", back_populates="findings")
    rule = relationship("Rule", back_populates="findings")
