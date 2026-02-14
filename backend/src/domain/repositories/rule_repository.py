from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from ..entities.rule import Rule


class RuleRepository(ABC):
    """Port (Interface) for Rule repository"""
    
    @abstractmethod
    async def create(self, rule: Rule) -> Rule:
        pass
    
    @abstractmethod
    async def get_by_id(self, rule_id: UUID) -> Optional[Rule]:
        pass
    
    @abstractmethod
    async def get_by_organization(self, org_id: UUID) -> List[Rule]:
        pass
    
    @abstractmethod
    async def get_active_by_audit_type(self, org_id: UUID, audit_type: str) -> List[Rule]:
        """Get active rules for specific audit type"""
        pass
    
    @abstractmethod
    async def update(self, rule: Rule) -> Rule:
        pass
    
    @abstractmethod
    async def delete(self, rule_id: UUID) -> bool:
        pass
