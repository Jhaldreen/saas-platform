from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)

class OrganizationResponse(OrganizationBase):
    id: UUID
    owner_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrganizationListResponse(BaseModel):
    organizations: list[OrganizationResponse]
    total: int
