from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from ....application.dto import RuleCreateDTO, RuleUpdateDTO, RuleResponseDTO, RuleListResponse
from ....application.use_cases import CreateRuleUseCase
from ....domain.entities import User
from ....domain.repositories import RuleRepository, OrganizationRepository
from ....domain.exceptions import EntityNotFoundError
from ..dependencies import (
    get_create_rule_use_case,
    get_current_user,
    get_rule_repository,
    get_organization_repository
)

router = APIRouter(prefix="/rules", tags=["Rules"])


@router.post("", response_model=RuleResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_rule(
    data: RuleCreateDTO,
    current_user: User = Depends(get_current_user),
    use_case: CreateRuleUseCase = Depends(get_create_rule_use_case),
    org_repository: OrganizationRepository = Depends(get_organization_repository)
):
    """
    Create a new audit rule
    
    Rules define criteria for automatically detecting issues in audits.
    
    Example conditions:
    ```json
    {
        "field": "cost",
        "operator": ">",
        "threshold": 1000
    }
    ```
    
    Supported operators: >, <, >=, <=, ==, !=
    """
    # Verify organization ownership
    org = await org_repository.get_by_id(data.organization_id)
    if not org or org.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Validate audit_type
    if data.audit_type not in ["cloud", "hospitality", "business"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid audit_type. Must be: cloud, hospitality, or business"
        )
    
    # Validate severity
    if data.severity not in ["low", "medium", "high", "critical"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid severity. Must be: low, medium, high, or critical"
        )
    
    # Create rule
    try:
        rule = await use_case.execute(
            organization_id=data.organization_id,
            name=data.name,
            audit_type=data.audit_type,
            conditions=data.conditions,
            severity=data.severity,
            created_by=current_user.id,
            description=data.description
        )
        
        return RuleResponseDTO.from_orm(rule)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=RuleListResponse)
async def list_rules(
    organization_id: UUID,
    current_user: User = Depends(get_current_user),
    rule_repository: RuleRepository = Depends(get_rule_repository),
    org_repository: OrganizationRepository = Depends(get_organization_repository)
):
    """
    List all rules for an organization
    
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
    
    # Get rules
    rules = await rule_repository.get_by_organization(organization_id)
    
    return RuleListResponse(
        rules=[RuleResponseDTO.from_orm(rule) for rule in rules],
        total=len(rules)
    )


@router.put("/{rule_id}", response_model=RuleResponseDTO)
async def update_rule(
    rule_id: UUID,
    data: RuleUpdateDTO,
    current_user: User = Depends(get_current_user),
    rule_repository: RuleRepository = Depends(get_rule_repository),
    org_repository: OrganizationRepository = Depends(get_organization_repository)
):
    """
    Update an existing rule
    
    All fields are optional - only provided fields will be updated.
    """
    # Get rule
    rule = await rule_repository.get_by_id(rule_id)
    
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    
    # Verify user owns the organization
    org = await org_repository.get_by_id(rule.organization_id)
    if not org or org.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    
    # Update fields
    if data.name is not None:
        rule.name = data.name
    if data.conditions is not None:
        rule.conditions = data.conditions
    if data.severity is not None:
        from ....domain.entities.rule import RuleSeverity
        rule.update_severity(RuleSeverity(data.severity))
    if data.is_active is not None:
        if data.is_active:
            rule.activate()
        else:
            rule.deactivate()
    
    # Save changes
    updated_rule = await rule_repository.update(rule)
    
    return RuleResponseDTO.from_orm(updated_rule)


@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(
    rule_id: UUID,
    current_user: User = Depends(get_current_user),
    rule_repository: RuleRepository = Depends(get_rule_repository),
    org_repository: OrganizationRepository = Depends(get_organization_repository)
):
    """
    Delete a rule
    
    This will also remove the rule from any future audit processing.
    Existing findings linked to this rule will remain.
    """
    # Get rule
    rule = await rule_repository.get_by_id(rule_id)
    
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    
    # Verify user owns the organization
    org = await org_repository.get_by_id(rule.organization_id)
    if not org or org.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rule not found"
        )
    
    # Delete rule
    await rule_repository.delete(rule_id)
    
    return None
