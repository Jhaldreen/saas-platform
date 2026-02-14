from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from uuid import UUID
from typing import Optional
import os

from ....application.dto import AuditResponseDTO, AuditListResponse, FindingListResponse, FindingResponseDTO
from ....application.use_cases import (
    CreateAuditUseCase,
    GetAuditFindingsUseCase
)
from ....domain.entities import User, AuditType
from ....domain.repositories import AuditRepository, OrganizationRepository
from ....domain.exceptions import EntityNotFoundError
from ..dependencies import (
    get_create_audit_use_case,
    get_audit_findings_use_case,
    get_current_user,
    get_audit_repository,
    get_organization_repository
)

router = APIRouter(prefix="/audits", tags=["Audits"])

# File upload configuration
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".csv", ".xlsx"}

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=AuditResponseDTO, status_code=status.HTTP_201_CREATED)
async def upload_audit(
    organization_id: UUID = Form(...),
    audit_type: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    use_case: CreateAuditUseCase = Depends(get_create_audit_use_case),
    org_repository: OrganizationRepository = Depends(get_organization_repository)
):
    """
    Upload a CSV file for audit analysis
    
    - **organization_id**: UUID of the organization
    - **audit_type**: Type of audit (cloud, hospitality, business)
    - **file**: CSV file to analyze
    """
    # Verify organization ownership
    org = await org_repository.get_by_id(organization_id)
    if not org or org.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
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
    """
    List all audits for user's organizations
    
    Optionally filter by organization_id
    """
    # Get user's organizations
    user_orgs = await org_repository.get_by_owner(current_user.id)
    user_org_ids = [org.id for org in user_orgs]
    
    if not user_org_ids:
        return AuditListResponse(audits=[], total=0)
    
    # Filter by specific organization if provided
    if organization_id:
        if organization_id not in user_org_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        audits = await audit_repository.get_by_organization(organization_id)
    else:
        # Get audits from all user's organizations
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
    """
    Get details of a specific audit
    """
    audit = await audit_repository.get_by_id(audit_id)
    
    if not audit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit not found"
        )
    
    # Verify user owns the organization
    org = await org_repository.get_by_id(audit.organization_id)
    if not org or org.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit not found"
        )
    
    return AuditResponseDTO.from_orm(audit)


@router.get("/{audit_id}/findings", response_model=FindingListResponse)
async def get_audit_findings(
    audit_id: UUID,
    current_user: User = Depends(get_current_user),
    use_case: GetAuditFindingsUseCase = Depends(get_audit_findings_use_case),
    audit_repository: AuditRepository = Depends(get_audit_repository),
    org_repository: OrganizationRepository = Depends(get_organization_repository)
):
    """
    Get all findings for a specific audit
    
    Returns list of issues/problems found during the audit.
    """
    # Verify audit exists and user has access
    audit = await audit_repository.get_by_id(audit_id)
    
    if not audit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit not found"
        )
    
    # Verify user owns the organization
    org = await org_repository.get_by_id(audit.organization_id)
    if not org or org.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit not found"
        )
    
    # Get findings
    findings = await use_case.execute(audit_id=audit_id)
    
    return FindingListResponse(
        findings=[FindingResponseDTO.from_orm(finding) for finding in findings],
        total=len(findings)
    )
