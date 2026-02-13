from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

from ..models.audit import AuditType, AuditStatus

class AuditBase(BaseModel):
    audit_type: AuditType
    file_name: str

class AuditCreate(AuditBase):
    organization_id: UUID

class AuditResponse(AuditBase):
    id: UUID
    organization_id: UUID
    file_path: str
    total_cost_or_revenue: Optional[float] = None
    optimization_score: Optional[int] = None
    status: AuditStatus
    error_message: Optional[str] = None
    created_at: datetime
    created_by: UUID
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class AuditListResponse(BaseModel):
    audits: list[AuditResponse]
    total: int

class AuditDetailResponse(AuditResponse):
    findings_count: int = 0
    
class AuditMetrics(BaseModel):
    total_audits: int
    completed_audits: int
    failed_audits: int
    avg_optimization_score: Optional[float]
    total_savings: Optional[float]
