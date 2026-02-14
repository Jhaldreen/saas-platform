from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional


@dataclass
class Organization:
    """Organization domain entity"""
    
    id: UUID
    name: str
    owner_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    def can_be_deleted(self) -> bool:
        """Business rule: Organizations can always be deleted by owner"""
        return True
    
    def is_owned_by(self, user_id: UUID) -> bool:
        """Check if user owns this organization"""
        return self.owner_id == user_id
