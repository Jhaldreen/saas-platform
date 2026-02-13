from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class FindingBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: str
    cost_impact: Optional[float] = None
    recommendation: Optional[str] = None

class FindingCreate(FindingBase):
    audit_id: UUID
    rule_id: Optional[UUID] = None
    evidence: Optional[Dict[str, Any]] = None

class FindingResponse(FindingBase):
    id: UUID
    audit_id: UUID
    rule_id: Optional[UUID] = None
    evidence: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class FindingListResponse(BaseModel):
    findings: list[FindingResponse]
    total: int
