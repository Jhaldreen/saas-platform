from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from ..entities.organization import Organization


class OrganizationRepository(ABC):
    """Port (Interface) for Organization repository"""
    
    @abstractmethod
    async def create(self, organization: Organization) -> Organization:
        """Create a new organization"""
        pass
    
    @abstractmethod
    async def get_by_id(self, org_id: UUID) -> Optional[Organization]:
        """Get organization by ID"""
        pass
    
    @abstractmethod
    async def get_by_owner(self, owner_id: UUID) -> List[Organization]:
        """Get all organizations owned by user"""
        pass
    
    @abstractmethod
    async def update(self, organization: Organization) -> Organization:
        """Update organization"""
        pass
    
    @abstractmethod
    async def delete(self, org_id: UUID) -> bool:
        """Delete organization"""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[Organization]:
        """List all organizations"""
        pass
