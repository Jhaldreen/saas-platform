from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from ..entities.audit import Audit, AuditStatus


class AuditRepository(ABC):
    """Port (Interface) for Audit repository"""
    
    @abstractmethod
    async def create(self, audit: Audit) -> Audit:
        """Create a new audit"""
        pass
    
    @abstractmethod
    async def get_by_id(self, audit_id: UUID) -> Optional[Audit]:
        """Get audit by ID"""
        pass
    
    @abstractmethod
    async def get_by_organization(self, org_id: UUID) -> List[Audit]:
        """Get all audits for an organization"""
        pass
    
    @abstractmethod
    async def get_by_status(self, status: AuditStatus) -> List[Audit]:
        """Get audits by status"""
        pass
    
    @abstractmethod
    async def update(self, audit: Audit) -> Audit:
        """Update audit"""
        pass
    
    @abstractmethod
    async def delete(self, audit_id: UUID) -> bool:
        """Delete audit"""
        pass
    
    @abstractmethod
    async def count_by_organization(self, org_id: UUID) -> int:
        """Count audits for organization"""
        pass
