from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

from ..models import RuleSeverity

class RuleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    audit_type: str  # cloud, hospitality, business
    conditions: Dict[str, Any]  # JSON conditions
    severity: RuleSeverity = RuleSeverity.MEDIUM
    is_active: bool = True

class RuleCreate(RuleBase):
    organization_id: UUID

class RuleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    conditions: Optional[Dict[str, Any]] = None
    severity: Optional[RuleSeverity] = None
    is_active: Optional[bool] = None

class RuleResponse(RuleBase):
    id: UUID
    organization_id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    
    class Config:
        from_attributes = True

class RuleListResponse(BaseModel):
    rules: list[RuleResponse]
    total: int
