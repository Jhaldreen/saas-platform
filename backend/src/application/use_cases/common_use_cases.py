# Remaining use cases - can be expanded similarly

from uuid import uuid4, UUID
from datetime import datetime
from typing import List

from ...domain.entities import Organization, Audit, Rule, Finding
from ...domain.entities.audit import AuditType, AuditStatus
from ...domain.repositories import (
    OrganizationRepository,
    AuditRepository,
    RuleRepository,
    FindingRepository
)
from ...domain.services.audit_service import AuditService
from ...domain.exceptions import EntityNotFoundError, UnauthorizedError


class CreateOrganizationUseCase:
    def __init__(self, org_repository: OrganizationRepository):
        self.org_repository = org_repository
    
    async def execute(self, name: str, owner_id: UUID) -> Organization:
        org = Organization(
            id=uuid4(),
            name=name,
            owner_id=owner_id,
            created_at=datetime.utcnow()
        )
        return await self.org_repository.create(org)


class GetUserOrganizationsUseCase:
    def __init__(self, org_repository: OrganizationRepository):
        self.org_repository = org_repository
    
    async def execute(self, owner_id: UUID) -> List[Organization]:
        return await self.org_repository.get_by_owner(owner_id)


class CreateAuditUseCase:
    def __init__(self, audit_repository: AuditRepository):
        self.audit_repository = audit_repository
    
    async def execute(
        self,
        organization_id: UUID,
        audit_type: AuditType,
        file_name: str,
        file_path: str,
        created_by: UUID
    ) -> Audit:
        audit = Audit(
            id=uuid4(),
            organization_id=organization_id,
            audit_type=audit_type,
            file_name=file_name,
            file_path=file_path,
            status=AuditStatus.PENDING,
            created_by=created_by,
            created_at=datetime.utcnow()
        )
        return await self.audit_repository.create(audit)


class ProcessAuditUseCase:
    """Process audit with CSV data and rules"""
    
    def __init__(
        self,
        audit_repository: AuditRepository,
        rule_repository: RuleRepository,
        finding_repository: FindingRepository,
        audit_service: AuditService
    ):
        self.audit_repository = audit_repository
        self.rule_repository = rule_repository
        self.finding_repository = finding_repository
        self.audit_service = audit_service
    
    async def execute(self, audit_id: UUID, csv_data: List[dict]) -> Audit:
        # Get audit
        audit = await self.audit_repository.get_by_id(audit_id)
        if not audit:
            raise EntityNotFoundError("Audit", str(audit_id))
        
        # Mark as processing
        audit.mark_as_processing()
        await self.audit_repository.update(audit)
        
        try:
            # Get active rules for this audit type
            rules = await self.rule_repository.get_active_by_audit_type(
                audit.organization_id,
                audit.audit_type.value
            )
            
            # Process data and generate findings
            findings = self.audit_service.process_csv_data(audit, rules, csv_data)
            
            # Save findings
            for finding in findings:
                await self.finding_repository.create(finding)
            
            # Calculate metrics
            score = self.audit_service.calculate_optimization_score(findings)
            total_cost = self.audit_service.calculate_total_cost_impact(findings)
            
            # Mark as completed
            audit.mark_as_completed(score, total_cost)
            
        except Exception as e:
            # Mark as failed
            audit.mark_as_failed(str(e))
        
        return await self.audit_repository.update(audit)


class CreateRuleUseCase:
    def __init__(self, rule_repository: RuleRepository):
        self.rule_repository = rule_repository
    
    async def execute(
        self,
        organization_id: UUID,
        name: str,
        audit_type: str,
        conditions: dict,
        severity: str,
        created_by: UUID,
        description: str = None
    ) -> Rule:
        from ...domain.entities.rule import RuleSeverity
        
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


class GetAuditFindingsUseCase:
    def __init__(self, finding_repository: FindingRepository):
        self.finding_repository = finding_repository
    
    async def execute(self, audit_id: UUID) -> List[Finding]:
        return await self.finding_repository.get_by_audit(audit_id)
