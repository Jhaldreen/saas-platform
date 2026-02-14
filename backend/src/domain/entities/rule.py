from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from enum import Enum
from typing import Dict, Any, Optional


class RuleSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Rule:
    """Rule domain entity - Dynamic audit rules"""
    
    id: UUID
    organization_id: UUID
    name: str
    audit_type: str
    conditions: Dict[str, Any]
    severity: RuleSeverity
    is_active: bool
    created_by: UUID
    created_at: datetime
    description: Optional[str] = None
    updated_at: Optional[datetime] = None
    
    def activate(self) -> None:
        """Business logic: Activate rule"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Business logic: Deactivate rule"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def update_severity(self, new_severity: RuleSeverity) -> None:
        """Business logic: Update rule severity"""
        self.severity = new_severity
        self.updated_at = datetime.utcnow()
    
    def matches_audit_type(self, audit_type: str) -> bool:
        """Check if rule applies to audit type"""
        return self.audit_type == audit_type
    
    def evaluate(self, data: Dict[str, Any]) -> bool:
        """
        Evaluate if data matches rule conditions
        Simple implementation - can be extended
        """
        if not self.is_active:
            return False
        
        field = self.conditions.get("field")
        operator = self.conditions.get("operator")
        threshold = self.conditions.get("threshold")
        
        if not all([field, operator, threshold]):
            return False
        
        value = data.get(field)
        if value is None:
            return False
        
        try:
            if operator == ">":
                return float(value) > float(threshold)
            elif operator == "<":
                return float(value) < float(threshold)
            elif operator == ">=":
                return float(value) >= float(threshold)
            elif operator == "<=":
                return float(value) <= float(threshold)
            elif operator == "==":
                return str(value) == str(threshold)
            elif operator == "!=":
                return str(value) != str(threshold)
        except (ValueError, TypeError):
            return False
        
        return False
