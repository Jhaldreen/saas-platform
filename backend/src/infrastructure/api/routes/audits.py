from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime
import os
import pandas as pd

from ....application.dto import AuditResponseDTO, AuditListResponse, FindingListResponse, FindingResponseDTO
from ....application.use_cases import CreateAuditUseCase, GetAuditFindingsUseCase
from ....domain.entities import User, AuditType, AuditStatus
from ....domain.entities.finding import Finding
from ....domain.repositories import AuditRepository, OrganizationRepository, RuleRepository, FindingRepository
from ....domain.exceptions import EntityNotFoundError
from ..dependencies import (
    get_create_audit_use_case,
    get_audit_findings_use_case,
    get_current_user,
    get_audit_repository,
    get_organization_repository,
    get_rule_repository,
    get_finding_repository
)

router = APIRouter(prefix="/audits", tags=["Audits"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".csv", ".xlsx"}

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=AuditResponseDTO, status_code=status.HTTP_201_CREATED)
async def upload_audit(
    organization_id: UUID = Form(...),
    audit_type: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    use_case: CreateAuditUseCase = Depends(get_create_audit_use_case),
    org_repository: OrganizationRepository = Depends(get_organization_repository),
    audit_repository: AuditRepository = Depends(get_audit_repository),
    rule_repository: RuleRepository = Depends(get_rule_repository),
    finding_repository: FindingRepository = Depends(get_finding_repository)
):
    """Upload a CSV file for audit analysis and process immediately"""
    
    # Verify organization ownership
    org = await org_repository.get_by_id(organization_id)
    if not org or org.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Read and validate file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Save file
    file_path = os.path.join(UPLOAD_DIR, f"{organization_id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Validate audit_type
    try:
        audit_type_enum = AuditType(audit_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid audit_type. Must be one of: cloud, hospitality, business"
        )
    
    # Create audit
    try:
        audit = await use_case.execute(
            organization_id=organization_id,
            audit_type=audit_type_enum,
            file_name=file.filename,
            file_path=file_path,
            created_by=current_user.id
        )
        
        # PROCESS IMMEDIATELY
        try:
            # Read CSV
            df = pd.read_csv(file_path)
            csv_data = df.to_dict('records')
            
            # Mark as processing
            audit.status = AuditStatus.PROCESSING
            await audit_repository.update(audit)
            
            # Get active rules
            rules = await rule_repository.get_active_by_audit_type(
                audit.organization_id,
                audit.audit_type.value
            )
            
            # Process data
            findings = []
            total_cost = 0.0
            
            for row in csv_data:
                for rule in rules:
                    # Evaluate rule
                    if rule.evaluate(row):
                        finding = Finding(
                            id=uuid4(),
                            audit_id=audit.id,
                            rule_id=rule.id,
                            title=f"{rule.name}",
                            severity=rule.severity,
                            description=rule.description or f"Issue detected by rule: {rule.name}",
                            evidence=row,
                            recommendation=f"Please review and address this finding based on rule criteria",
                            created_at=datetime.utcnow()
                        )
                        
                        # Try to get cost impact
                        cost_field = rule.conditions.get('field', 'cost')
                        if cost_field in row:
                            try:
                                finding.cost_impact = float(row[cost_field])
                                total_cost += finding.cost_impact
                            except:
                                pass
                        
                        findings.append(finding)
                        await finding_repository.create(finding)
            
            # Calculate optimization score (0-100)
            severity_weights = {'low': 2, 'medium': 5, 'high': 10, 'critical': 15}
            penalty = sum(severity_weights.get(f.severity.value, 5) for f in findings)
            score = max(0, min(100, 100 - penalty))
            
            # Update audit
            audit.mark_as_completed(score, total_cost if total_cost > 0 else None)
            audit = await audit_repository.update(audit)
            
        except Exception as e:
            # Mark as failed
            audit.mark_as_failed(str(e))
            await audit_repository.update(audit)
        
        return AuditResponseDTO.from_orm(audit)
        
    except Exception as e:
        # Clean up file if audit creation fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=AuditListResponse)
async def list_audits(
    organization_id: Optional[UUID] = None,
    current_user: User = Depends(get_current_user),
    audit_repository: AuditRepository = Depends(get_audit_repository),
    org_repository: OrganizationRepository = Depends(get_organization_repository)
):
    """List all audits for user's organizations"""
    user_orgs = await org_repository.get_by_owner(current_user.id)
    user_org_ids = [org.id for org in user_orgs]
    
    if not user_org_ids:
        return AuditListResponse(audits=[], total=0)
    
    if organization_id:
        if organization_id not in user_org_ids:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        audits = await audit_repository.get_by_organization(organization_id)
    else:
        all_audits = []
        for org_id in user_org_ids:
            org_audits = await audit_repository.get_by_organization(org_id)
            all_audits.extend(org_audits)
        audits = all_audits
    
    return AuditListResponse(
        audits=[AuditResponseDTO.from_orm(audit) for audit in audits],
        total=len(audits)
    )


@router.get("/{audit_id}", response_model=AuditResponseDTO)
async def get_audit(
    audit_id: UUID,
    current_user: User = Depends(get_current_user),
    audit_repository: AuditRepository = Depends(get_audit_repository),
    org_repository: OrganizationRepository = Depends(get_organization_repository)
):
    """Get details of a specific audit"""
    audit = await audit_repository.get_by_id(audit_id)
    
    if not audit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit not found")
    
    org = await org_repository.get_by_id(audit.organization_id)
    if not org or org.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit not found")
    
    return AuditResponseDTO.from_orm(audit)


@router.get("/{audit_id}/findings", response_model=FindingListResponse)
async def get_audit_findings(
    audit_id: UUID,
    current_user: User = Depends(get_current_user),
    use_case: GetAuditFindingsUseCase = Depends(get_audit_findings_use_case),
    audit_repository: AuditRepository = Depends(get_audit_repository),
    org_repository: OrganizationRepository = Depends(get_organization_repository)
):
    """Get all findings for a specific audit"""
    audit = await audit_repository.get_by_id(audit_id)
    
    if not audit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit not found")
    
    org = await org_repository.get_by_id(audit.organization_id)
    if not org or org.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit not found")
    
    findings = await use_case.execute(audit_id=audit_id)
    
    return FindingListResponse(
        findings=[FindingResponseDTO.from_orm(finding) for finding in findings],
        total=len(findings)
    )

@router.get("/{audit_id}/data")
async def get_audit_data(
    audit_id: UUID,
    current_user: User = Depends(get_current_user),
    audit_repository: AuditRepository = Depends(get_audit_repository),
    org_repository: OrganizationRepository = Depends(get_organization_repository)
):
    
    audit = await audit_repository.get_by_id(audit_id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    org = await org_repository.get_by_id(audit.organization_id)
    if not org or org.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    if not os.path.exists(audit.file_path):
        raise HTTPException(status_code=404, detail="CSV file not found")
    
    df = pd.read_csv(audit.file_path)
    return {"data": df.to_dict('records'), "columns": list(df.columns)}