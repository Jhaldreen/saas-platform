from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from ....application.dto import OrganizationCreateDTO, OrganizationResponseDTO, OrganizationListResponse
from ....application.use_cases import CreateOrganizationUseCase, GetUserOrganizationsUseCase
from ....domain.exceptions import EntityNotFoundError
from ..dependencies import get_create_organization_use_case, get_user_organizations_use_case, get_current_user
from ....domain.entities import User

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("", response_model=OrganizationResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_organization(
    data: OrganizationCreateDTO,
    current_user: User = Depends(get_current_user),
    use_case: CreateOrganizationUseCase = Depends(get_create_organization_use_case)
):
    """
    Create a new organization
    
    The authenticated user becomes the owner of the organization.
    """
    try:
        organization = await use_case.execute(
            name=data.name,
            owner_id=current_user.id
        )
        
        return OrganizationResponseDTO.from_orm(organization)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=OrganizationListResponse)
async def list_organizations(
    current_user: User = Depends(get_current_user),
    use_case: GetUserOrganizationsUseCase = Depends(get_user_organizations_use_case)
):
    """
    List all organizations owned by the current user
    """
    organizations = await use_case.execute(owner_id=current_user.id)
    
    return OrganizationListResponse(
        organizations=[OrganizationResponseDTO.from_orm(org) for org in organizations],
        total=len(organizations)
    )


@router.get("/{org_id}", response_model=OrganizationResponseDTO)
async def get_organization(
    org_id: UUID,
    current_user: User = Depends(get_current_user),
    use_case: GetUserOrganizationsUseCase = Depends(get_user_organizations_use_case)
):
    """
    Get details of a specific organization
    
    Only returns organizations owned by the current user.
    """
    organizations = await use_case.execute(owner_id=current_user.id)
    
    # Find the requested organization
    organization = next((org for org in organizations if org.id == org_id), None)
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    return OrganizationResponseDTO.from_orm(organization)
