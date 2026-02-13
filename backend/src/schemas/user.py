from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

from ..models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.MEMBER

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.MEMBER

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None

class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse
