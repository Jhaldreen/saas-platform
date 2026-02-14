from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Dict, Any, Optional


@dataclass
class Finding:
    """Finding domain entity - Result from audit analysis"""
    
    id: UUID
    audit_id: UUID
    title: str
    severity: str
    created_at: datetime
    rule_id: Optional[UUID] = None
    description: Optional[str] = None
    cost_impact: Optional[float] = None
    evidence: Optional[Dict[str, Any]] = None
    recommendation: Optional[str] = None
    
    def has_significant_impact(self, threshold: float = 1000.0) -> bool:
        """Business rule: Check if finding has significant cost impact"""
        if self.cost_impact is None:
            return False
        return abs(self.cost_impact) >= threshold
    
    def is_critical(self) -> bool:
        """Check if finding is critical severity"""
        return self.severity.lower() == "critical"
