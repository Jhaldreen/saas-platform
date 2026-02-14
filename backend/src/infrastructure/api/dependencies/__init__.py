from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from uuid import UUID

from ...database import get_db
from ...security.jwt import decode_access_token
from ...persistence.repositories import (
    SQLAlchemyUserRepository,
    SQLAlchemyOrganizationRepository,
    SQLAlchemyAuditRepository,
    SQLAlchemyRuleRepository,
    SQLAlchemyFindingRepository
)
from ....domain.services import AuthenticationService, AuditService
from ....domain.entities.user import User
from ....application.use_cases import *

security = HTTPBearer()

# ============ REPOSITORIES ============

def get_user_repository(db: Session = Depends(get_db)):
    return SQLAlchemyUserRepository(db)


def get_organization_repository(db: Session = Depends(get_db)):
    return SQLAlchemyOrganizationRepository(db)


def get_audit_repository(db: Session = Depends(get_db)):
    return SQLAlchemyAuditRepository(db)


def get_rule_repository(db: Session = Depends(get_db)):
    return SQLAlchemyRuleRepository(db)


def get_finding_repository(db: Session = Depends(get_db)):
    return SQLAlchemyFindingRepository(db)


# ============ SERVICES ============

def get_auth_service():
    return AuthenticationService()


def get_audit_service():
    return AuditService()


# ============ USE CASES ============

def get_register_user_use_case(
    user_repo=Depends(get_user_repository),
    auth_service=Depends(get_auth_service)
):
    return RegisterUserUseCase(user_repo, auth_service)


def get_login_user_use_case(
    user_repo=Depends(get_user_repository),
    auth_service=Depends(get_auth_service)
):
    return LoginUserUseCase(user_repo, auth_service)


def get_create_organization_use_case(org_repo=Depends(get_organization_repository)):
    return CreateOrganizationUseCase(org_repo)


def get_user_organizations_use_case(org_repo=Depends(get_organization_repository)):
    return GetUserOrganizationsUseCase(org_repo)


def get_create_audit_use_case(audit_repo=Depends(get_audit_repository)):
    return CreateAuditUseCase(audit_repo)


def get_process_audit_use_case(
    audit_repo=Depends(get_audit_repository),
    rule_repo=Depends(get_rule_repository),
    finding_repo=Depends(get_finding_repository),
    audit_service=Depends(get_audit_service)
):
    return ProcessAuditUseCase(audit_repo, rule_repo, finding_repo, audit_service)


def get_create_rule_use_case(rule_repo=Depends(get_rule_repository)):
    return CreateRuleUseCase(rule_repo)


def get_audit_findings_use_case(finding_repo=Depends(get_finding_repository)):
    return GetAuditFindingsUseCase(finding_repo)


# ============ CURRENT USER ============

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repo=Depends(get_user_repository)
) -> User:
    """Get current authenticated user"""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user_id = UUID(payload["sub"])
    user = await user_repo.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user
