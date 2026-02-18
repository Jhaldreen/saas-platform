from uuid import uuid4, UUID
from datetime import datetime
from typing import List, Dict, Any

from ...domain.entities.rule import Rule, RuleSeverity
from ...domain.repositories.rule_repository import RuleRepository
from ...domain.exceptions import EntityNotFoundError


class CreateRuleUseCase:
    """Use case: Create a new rule"""
    
    def __init__(self, rule_repository: RuleRepository):
        self.rule_repository = rule_repository
    
    async def execute(
        self,
        organization_id: UUID,
        name: str,
        audit_type: str,
        conditions: Dict[str, Any],
        severity: str,
        created_by: UUID,
        description: str = None
    ) -> Rule:
        rule = Rule(
            id=uuid4(),
            organization_id=organization_id,
            name=name,
            audit_type=audit_type,
            conditions=conditions,
            severity=RuleSeverity(severity),
            is_active=True,
            created_by=created_by,
            created_at=datetime.utcnow(),
            description=description
        )
        return await self.rule_repository.create(rule)


class GetRulesByOrganizationUseCase:
    """Use case: Get all rules for an organization"""
    
    def __init__(self, rule_repository: RuleRepository):
        self.rule_repository = rule_repository
    
    async def execute(self, organization_id: UUID) -> List[Rule]:
        return await self.rule_repository.get_by_organization(organization_id)


class GetRuleByIdUseCase:
    """Use case: Get rule by ID"""
    
    def __init__(self, rule_repository: RuleRepository):
        self.rule_repository = rule_repository
    
    async def execute(self, rule_id: UUID) -> Rule:
        rule = await self.rule_repository.get_by_id(rule_id)
        if not rule:
            raise EntityNotFoundError("Rule", str(rule_id))
        return rule


class UpdateRuleUseCase:
    """Use case: Update rule"""
    
    def __init__(self, rule_repository: RuleRepository):
        self.rule_repository = rule_repository
    
    async def execute(
        self,
        rule_id: UUID,
        name: str = None,
        conditions: Dict[str, Any] = None,
        severity: str = None,
        is_active: bool = None,
        description: str = None
    ) -> Rule:
        rule = await self.rule_repository.get_by_id(rule_id)
        if not rule:
            raise EntityNotFoundError("Rule", str(rule_id))
        
        # Update fields
        if name is not None:
            rule.name = name
        if conditions is not None:
            rule.conditions = conditions
        if severity is not None:
            rule.update_severity(RuleSeverity(severity))
        if is_active is not None:
            if is_active:
                rule.activate()
            else:
                rule.deactivate()
        if description is not None:
            rule.description = description
        
        return await self.rule_repository.update(rule)


class DeleteRuleUseCase:
    """Use case: Delete rule"""
    
    def __init__(self, rule_repository: RuleRepository):
        self.rule_repository = rule_repository
    
    async def execute(self, rule_id: UUID) -> bool:
        rule = await self.rule_repository.get_by_id(rule_id)
        if not rule:
            raise EntityNotFoundError("Rule", str(rule_id))
        
        return await self.rule_repository.delete(rule_id)


class GetActiveRulesByAuditTypeUseCase:
    """Use case: Get active rules for specific audit type"""
    
    def __init__(self, rule_repository: RuleRepository):
        self.rule_repository = rule_repository
    
    async def execute(self, organization_id: UUID, audit_type: str) -> List[Rule]:
        return await self.rule_repository.get_active_by_audit_type(organization_id, audit_type)
