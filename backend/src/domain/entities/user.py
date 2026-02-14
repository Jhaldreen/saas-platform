from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


@dataclass
class User:
    """User domain entity - Pure business logic, no framework dependencies"""
    
    id: UUID
    email: str
    password_hash: str
    role: UserRole
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    def is_admin(self) -> bool:
        """Check if user has admin privileges"""
        return self.role == UserRole.ADMIN
    
    def can_create_organization(self) -> bool:
        """Business rule: Only admins and members can create organizations"""
        return self.role in [UserRole.ADMIN, UserRole.MEMBER]
    
    def can_manage_rules(self) -> bool:
        """Business rule: Only admins can manage audit rules"""
        return self.role == UserRole.ADMIN
