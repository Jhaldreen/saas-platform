# Application DTOs - Pydantic models for API

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID


# ============ USER DTOs ============
class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = "member"


class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str


class UserResponseDTO(BaseModel):
    id: UUID
    email: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponseDTO


# ============ ORGANIZATION DTOs ============
class OrganizationCreateDTO(BaseModel):
    name: str = Field(..., min_length=1)


class OrganizationResponseDTO(BaseModel):
    id: UUID
    name: str
    owner_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ AUDIT DTOs ============
class AuditCreateDTO(BaseModel):
    organization_id: UUID
    audit_type: str  # cloud, hospitality, business


class AuditResponseDTO(BaseModel):
    id: UUID
    organization_id: UUID
    audit_type: str
    file_name: str
    status: str
    total_cost_or_revenue: Optional[float] = None
    optimization_score: Optional[int] = None
    created_at: datetime
    created_by: UUID
    
    class Config:
        from_attributes = True


# ============ RULE DTOs ============
class RuleCreateDTO(BaseModel):
    organization_id: UUID
    name: str
    audit_type: str
    conditions: Dict[str, Any]
    severity: str
    description: Optional[str] = None


class RuleUpdateDTO(BaseModel):
    name: Optional[str] = None
    conditions: Optional[Dict[str, Any]] = None
    severity: Optional[str] = None
    is_active: Optional[bool] = None


class RuleResponseDTO(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    audit_type: str
    conditions: Dict[str, Any]
    severity: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ FINDING DTOs ============
class FindingResponseDTO(BaseModel):
    id: UUID
    audit_id: UUID
    title: str
    severity: str
    cost_impact: Optional[float] = None
    description: Optional[str] = None
    recommendation: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Organization List Response
class OrganizationListResponse(BaseModel):
    organizations: List[OrganizationResponseDTO]
    total: int

# Audit List Response
class AuditListResponse(BaseModel):
    audits: List[AuditResponseDTO]
    total: int

# Finding List Response
class FindingListResponse(BaseModel):
    findings: List[FindingResponseDTO]
    total: int

# Rule List Response
class RuleListResponse(BaseModel):
    rules: List[RuleResponseDTO]
    total: int