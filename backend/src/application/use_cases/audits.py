from uuid import uuid4, UUID
from datetime import datetime
from typing import List

from ...domain.entities.audit import Audit, AuditType, AuditStatus
from ...domain.entities.finding import Finding
from ...domain.repositories.audit_repository import AuditRepository
from ...domain.repositories.finding_repository import FindingRepository
from ...domain.repositories.rule_repository import RuleRepository
from ...domain.services.audit_service import AuditService
from ...domain.exceptions import EntityNotFoundError


class CreateAuditUseCase:
    """Use case: Create a new audit"""
    
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


class GetAuditsByOrganizationUseCase:
    """Use case: Get all audits for an organization"""
    
    def __init__(self, audit_repository: AuditRepository):
        self.audit_repository = audit_repository
    
    async def execute(self, organization_id: UUID) -> List[Audit]:
        return await self.audit_repository.get_by_organization(organization_id)


class GetAuditByIdUseCase:
    """Use case: Get audit by ID"""
    
    def __init__(self, audit_repository: AuditRepository):
        self.audit_repository = audit_repository
    
    async def execute(self, audit_id: UUID) -> Audit:
        audit = await self.audit_repository.get_by_id(audit_id)
        if not audit:
            raise EntityNotFoundError("Audit", str(audit_id))
        return audit


class ProcessAuditUseCase:
    """Use case: Process audit with CSV data and rules"""
    
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


class GetAuditFindingsUseCase:
    """Use case: Get all findings for an audit"""
    
    def __init__(self, finding_repository: FindingRepository):
        self.finding_repository = finding_repository
    
    async def execute(self, audit_id: UUID) -> List[Finding]:
        return await self.finding_repository.get_by_audit(audit_id)
