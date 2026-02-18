from uuid import UUID
from typing import Optional

from ...domain.entities import Rule
from ...domain.repositories import RuleRepository
from ...domain.exceptions import EntityNotFoundError


class UpdateRuleUseCase:
    """Use case: Update an existing rule"""
    
    def __init__(self, rule_repository: RuleRepository):
        self.rule_repository = rule_repository
    
    async def execute(
        self,
        rule_id: UUID,
        name: Optional[str] = None,
        conditions: Optional[dict] = None,
        severity: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Rule:
        """
        Update a rule with new values
        
        Args:
            rule_id: UUID of the rule to update
            name: New name (optional)
            conditions: New conditions (optional)
            severity: New severity (optional)
            is_active: New active status (optional)
            
        Returns:
            Updated rule
            
        Raises:
            EntityNotFoundError: If rule doesn't exist
        """
        # Get existing rule
        rule = await self.rule_repository.get_by_id(rule_id)
        if not rule:
            raise EntityNotFoundError("Rule", str(rule_id))
        
        # Update fields if provided
        if name is not None:
            rule.name = name
        
        if conditions is not None:
            rule.conditions = conditions
        
        if severity is not None:
            from ...domain.entities.rule import RuleSeverity
            rule.update_severity(RuleSeverity(severity))
        
        if is_active is not None:
            if is_active:
                rule.activate()
            else:
                rule.deactivate()
        
        # Save changes
        updated_rule = await self.rule_repository.update(rule)
        
        return updated_rule


class DeleteRuleUseCase:
    """Use case: Delete a rule"""
    
    def __init__(self, rule_repository: RuleRepository):
        self.rule_repository = rule_repository
    
    async def execute(self, rule_id: UUID) -> bool:
        """
        Delete a rule
        
        Args:
            rule_id: UUID of the rule to delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            EntityNotFoundError: If rule doesn't exist
        """
        # Verify rule exists
        rule = await self.rule_repository.get_by_id(rule_id)
        if not rule:
            raise EntityNotFoundError("Rule", str(rule_id))
        
        # Delete rule
        result = await self.rule_repository.delete(rule_id)
        
        return result
