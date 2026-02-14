from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from enum import Enum
from typing import Optional


class AuditType(str, Enum):
    CLOUD = "cloud"
    HOSPITALITY = "hospitality"
    BUSINESS = "business"


class AuditStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Audit:
    """Audit domain entity"""
    
    id: UUID
    organization_id: UUID
    audit_type: AuditType
    file_name: str
    file_path: str
    status: AuditStatus
    created_by: UUID
    created_at: datetime
    total_cost_or_revenue: Optional[float] = None
    optimization_score: Optional[int] = None
    error_message: Optional[str] = None
    completed_at: Optional[datetime] = None
    
    def mark_as_processing(self) -> None:
        """Business logic: Start processing"""
        if self.status != AuditStatus.PENDING:
            raise ValueError("Can only process pending audits")
        self.status = AuditStatus.PROCESSING
    
    def mark_as_completed(self, score: int, cost_or_revenue: float) -> None:
        """Business logic: Complete audit"""
        if self.status != AuditStatus.PROCESSING:
            raise ValueError("Can only complete processing audits")
        
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100")
        
        self.status = AuditStatus.COMPLETED
        self.optimization_score = score
        self.total_cost_or_revenue = cost_or_revenue
        self.completed_at = datetime.utcnow()
    
    def mark_as_failed(self, error: str) -> None:
        """Business logic: Mark as failed"""
        self.status = AuditStatus.FAILED
        self.error_message = error
        self.completed_at = datetime.utcnow()
    
    def is_editable(self) -> bool:
        """Business rule: Only pending audits can be edited"""
        return self.status == AuditStatus.PENDING
