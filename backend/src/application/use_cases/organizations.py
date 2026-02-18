from uuid import uuid4, UUID
from datetime import datetime
from typing import List

from ...domain.entities.organization import Organization
from ...domain.repositories.organization_repository import OrganizationRepository
from ...domain.exceptions import EntityNotFoundError


class CreateOrganizationUseCase:
    """Use case: Create a new organization"""
    
    def __init__(self, org_repository: OrganizationRepository):
        self.org_repository = org_repository
    
    async def execute(self, name: str, owner_id: UUID) -> Organization:
        organization = Organization(
            id=uuid4(),
            name=name,
            owner_id=owner_id,
            created_at=datetime.utcnow()
        )
        return await self.org_repository.create(organization)


class GetUserOrganizationsUseCase:
    """Use case: Get all organizations owned by a user"""
    
    def __init__(self, org_repository: OrganizationRepository):
        self.org_repository = org_repository
    
    async def execute(self, owner_id: UUID) -> List[Organization]:
        return await self.org_repository.get_by_owner(owner_id)


class GetOrganizationByIdUseCase:
    """Use case: Get organization by ID"""
    
    def __init__(self, org_repository: OrganizationRepository):
        self.org_repository = org_repository
    
    async def execute(self, org_id: UUID) -> Organization:
        org = await self.org_repository.get_by_id(org_id)
        if not org:
            raise EntityNotFoundError("Organization", str(org_id))
        return org


class UpdateOrganizationUseCase:
    """Use case: Update organization"""
    
    def __init__(self, org_repository: OrganizationRepository):
        self.org_repository = org_repository
    
    async def execute(self, org_id: UUID, name: str) -> Organization:
        org = await self.org_repository.get_by_id(org_id)
        if not org:
            raise EntityNotFoundError("Organization", str(org_id))
        
        org.name = name
        org.updated_at = datetime.utcnow()
        
        return await self.org_repository.update(org)


class DeleteOrganizationUseCase:
    """Use case: Delete organization"""
    
    def __init__(self, org_repository: OrganizationRepository):
        self.org_repository = org_repository
    
    async def execute(self, org_id: UUID) -> bool:
        org = await self.org_repository.get_by_id(org_id)
        if not org:
            raise EntityNotFoundError("Organization", str(org_id))
        
        return await self.org_repository.delete(org_id)
