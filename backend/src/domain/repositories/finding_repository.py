from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from ..entities.finding import Finding


class FindingRepository(ABC):
    """Port (Interface) for Finding repository"""
    
    @abstractmethod
    async def create(self, finding: Finding) -> Finding:
        pass
    
    @abstractmethod
    async def get_by_id(self, finding_id: UUID) -> Optional[Finding]:
        pass
    
    @abstractmethod
    async def get_by_audit(self, audit_id: UUID) -> List[Finding]:
        pass
    
    @abstractmethod
    async def get_by_severity(self, audit_id: UUID, severity: str) -> List[Finding]:
        pass
    
    @abstractmethod
    async def delete(self, finding_id: UUID) -> bool:
        pass
    
    @abstractmethod
    async def delete_by_audit(self, audit_id: UUID) -> int:
        """Delete all findings for an audit, return count deleted"""
        pass
