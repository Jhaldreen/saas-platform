from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from ....domain.entities import User, AuditStatus
from ....domain.repositories import (
    AuditRepository,
    FindingRepository,
    RuleRepository,
    OrganizationRepository
)
from ..dependencies import (
    get_current_user,
    get_audit_repository,
    get_finding_repository,
    get_rule_repository,
    get_organization_repository
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/metrics")
async def get_dashboard_metrics(
    organization_id: UUID,
    current_user: User = Depends(get_current_user),
    audit_repository: AuditRepository = Depends(get_audit_repository),
    finding_repository: FindingRepository = Depends(get_finding_repository),
    rule_repository: RuleRepository = Depends(get_rule_repository),
    org_repository: OrganizationRepository = Depends(get_organization_repository)
):
    """
    Get aggregated metrics for organization dashboard
    
    Returns:
    - Total number of audits
    - Number of completed audits
    - Total findings across all audits
    - Average optimization score
    - Number of active rules
    
    Query parameter:
    - **organization_id**: UUID of the organization (required)
    """
    # Verify organization ownership
    org = await org_repository.get_by_id(organization_id)
    if not org or org.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Get all audits for organization
    audits = await audit_repository.get_by_organization(organization_id)
    
    # Calculate metrics
    total_audits = len(audits)
    
    completed_audits = [
        audit for audit in audits 
        if audit.status == AuditStatus.COMPLETED
    ]
    completed_count = len(completed_audits)
    
    # Count total findings across all audits
    total_findings = 0
    for audit in audits:
        findings = await finding_repository.get_by_audit(audit.id)
        total_findings += len(findings)
    
    # Calculate average optimization score
    avg_score = None
    if completed_audits:
        scores = [
            audit.optimization_score 
            for audit in completed_audits 
            if audit.optimization_score is not None
        ]
        if scores:
            avg_score = sum(scores) / len(scores)
    
    # Count active rules
    all_rules = await rule_repository.get_by_organization(organization_id)
    active_rules = len([rule for rule in all_rules if rule.is_active])
    
    return {
        "total_audits": total_audits,
        "completed_audits": completed_count,
        "total_findings": total_findings,
        "avg_optimization_score": round(avg_score, 1) if avg_score else None,
        "active_rules": active_rules
    }
