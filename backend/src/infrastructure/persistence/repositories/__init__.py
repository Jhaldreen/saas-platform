# SQLAlchemy Repository Implementations

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ....domain.entities import User, Organization, Audit, Rule, Finding
from ....domain.entities.audit import AuditType, AuditStatus
from ....domain.entities.user import UserRole
from ....domain.entities.rule import RuleSeverity
from ....domain.repositories import (
    UserRepository,
    OrganizationRepository,
    AuditRepository,
    RuleRepository,
    FindingRepository
)
from ..models import (
    UserModel,
    OrganizationModel,
    AuditModel,
    RuleModel,
    FindingModel
)


# ============ MAPPERS ============

class UserMapper:
    @staticmethod
    def to_domain(model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            role=UserRole(model.role),
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    @staticmethod
    def to_model(entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            email=entity.email,
            password_hash=entity.password_hash,
            role=entity.role.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )


class OrganizationMapper:
    @staticmethod
    def to_domain(model: OrganizationModel) -> Organization:
        return Organization(
            id=model.id,
            name=model.name,
            owner_id=model.owner_id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    @staticmethod
    def to_model(entity: Organization) -> OrganizationModel:
        return OrganizationModel(
            id=entity.id,
            name=entity.name,
            owner_id=entity.owner_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )


class AuditMapper:
    @staticmethod
    def to_domain(model: AuditModel) -> Audit:
        return Audit(
            id=model.id,
            organization_id=model.organization_id,
            audit_type=AuditType(model.audit_type),
            file_name=model.file_name,
            file_path=model.file_path,
            status=AuditStatus(model.status),
            created_by=model.created_by,
            created_at=model.created_at,
            total_cost_or_revenue=model.total_cost_or_revenue,
            optimization_score=model.optimization_score,
            error_message=model.error_message,
            completed_at=model.completed_at
        )
    
    @staticmethod
    def to_model(entity: Audit) -> AuditModel:
        return AuditModel(
            id=entity.id,
            organization_id=entity.organization_id,
            audit_type=entity.audit_type.value,
            file_name=entity.file_name,
            file_path=entity.file_path,
            status=entity.status.value,
            created_by=entity.created_by,
            created_at=entity.created_at,
            total_cost_or_revenue=entity.total_cost_or_revenue,
            optimization_score=entity.optimization_score,
            error_message=entity.error_message,
            completed_at=entity.completed_at
        )


class RuleMapper:
    @staticmethod
    def to_domain(model: RuleModel) -> Rule:
        return Rule(
            id=model.id,
            organization_id=model.organization_id,
            name=model.name,
            audit_type=model.audit_type,
            conditions=model.conditions,
            severity=RuleSeverity(model.severity),
            is_active=model.is_active,
            created_by=model.created_by,
            created_at=model.created_at,
            description=model.description,
            updated_at=model.updated_at
        )
    
    @staticmethod
    def to_model(entity: Rule) -> RuleModel:
        return RuleModel(
            id=entity.id,
            organization_id=entity.organization_id,
            name=entity.name,
            audit_type=entity.audit_type,
            conditions=entity.conditions,
            severity=entity.severity.value,
            is_active=entity.is_active,
            created_by=entity.created_by,
            created_at=entity.created_at,
            description=entity.description,
            updated_at=entity.updated_at
        )


class FindingMapper:
    @staticmethod
    def to_domain(model: FindingModel) -> Finding:
        return Finding(
            id=model.id,
            audit_id=model.audit_id,
            title=model.title,
            severity=model.severity,
            created_at=model.created_at,
            rule_id=model.rule_id,
            description=model.description,
            cost_impact=model.cost_impact,
            evidence=model.evidence,
            recommendation=model.recommendation
        )
    
    @staticmethod
    def to_model(entity: Finding) -> FindingModel:
        return FindingModel(
            id=entity.id,
            audit_id=entity.audit_id,
            title=entity.title,
            severity=entity.severity,
            created_at=entity.created_at,
            rule_id=entity.rule_id,
            description=entity.description,
            cost_impact=entity.cost_impact,
            evidence=entity.evidence,
            recommendation=entity.recommendation
        )


# ============ REPOSITORIES ============

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, user: User) -> User:
        model = UserMapper.to_model(user)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return UserMapper.to_domain(model)
    
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        model = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        return UserMapper.to_domain(model) if model else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        model = self.session.query(UserModel).filter(UserModel.email == email).first()
        return UserMapper.to_domain(model) if model else None
    
    async def update(self, user: User) -> User:
        model = self.session.query(UserModel).filter(UserModel.id == user.id).first()
        if model:
            model.email = user.email
            model.password_hash = user.password_hash
            model.role = user.role.value
            self.session.commit()
            self.session.refresh(model)
        return UserMapper.to_domain(model)
    
    async def delete(self, user_id: UUID) -> bool:
        model = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False
    
    async def list_all(self) -> List[User]:
        models = self.session.query(UserModel).all()
        return [UserMapper.to_domain(m) for m in models]


class SQLAlchemyOrganizationRepository(OrganizationRepository):
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, organization: Organization) -> Organization:
        model = OrganizationMapper.to_model(organization)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return OrganizationMapper.to_domain(model)
    
    async def get_by_id(self, org_id: UUID) -> Optional[Organization]:
        model = self.session.query(OrganizationModel).filter(OrganizationModel.id == org_id).first()
        return OrganizationMapper.to_domain(model) if model else None
    
    async def get_by_owner(self, owner_id: UUID) -> List[Organization]:
        models = self.session.query(OrganizationModel).filter(OrganizationModel.owner_id == owner_id).all()
        return [OrganizationMapper.to_domain(m) for m in models]
    
    async def update(self, organization: Organization) -> Organization:
        model = self.session.query(OrganizationModel).filter(OrganizationModel.id == organization.id).first()
        if model:
            model.name = organization.name
            self.session.commit()
            self.session.refresh(model)
        return OrganizationMapper.to_domain(model)
    
    async def delete(self, org_id: UUID) -> bool:
        model = self.session.query(OrganizationModel).filter(OrganizationModel.id == org_id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False
    
    async def list_all(self) -> List[Organization]:
        models = self.session.query(OrganizationModel).all()
        return [OrganizationMapper.to_domain(m) for m in models]


class SQLAlchemyAuditRepository(AuditRepository):
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, audit: Audit) -> Audit:
        model = AuditMapper.to_model(audit)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return AuditMapper.to_domain(model)
    
    async def get_by_id(self, audit_id: UUID) -> Optional[Audit]:
        model = self.session.query(AuditModel).filter(AuditModel.id == audit_id).first()
        return AuditMapper.to_domain(model) if model else None
    
    async def get_by_organization(self, org_id: UUID) -> List[Audit]:
        models = self.session.query(AuditModel).filter(AuditModel.organization_id == org_id).all()
        return [AuditMapper.to_domain(m) for m in models]
    
    async def get_by_status(self, status: AuditStatus) -> List[Audit]:
        models = self.session.query(AuditModel).filter(AuditModel.status == status.value).all()
        return [AuditMapper.to_domain(m) for m in models]
    
    async def update(self, audit: Audit) -> Audit:
        model = self.session.query(AuditModel).filter(AuditModel.id == audit.id).first()
        if model:
            model.status = audit.status.value
            model.optimization_score = audit.optimization_score
            model.total_cost_or_revenue = audit.total_cost_or_revenue
            model.error_message = audit.error_message
            model.completed_at = audit.completed_at
            self.session.commit()
            self.session.refresh(model)
        return AuditMapper.to_domain(model)
    
    async def delete(self, audit_id: UUID) -> bool:
        model = self.session.query(AuditModel).filter(AuditModel.id == audit_id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False
    
    async def count_by_organization(self, org_id: UUID) -> int:
        return self.session.query(AuditModel).filter(AuditModel.organization_id == org_id).count()


class SQLAlchemyRuleRepository(RuleRepository):
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, rule: Rule) -> Rule:
        model = RuleMapper.to_model(rule)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return RuleMapper.to_domain(model)
    
    async def get_by_id(self, rule_id: UUID) -> Optional[Rule]:
        model = self.session.query(RuleModel).filter(RuleModel.id == rule_id).first()
        return RuleMapper.to_domain(model) if model else None
    
    async def get_by_organization(self, org_id: UUID) -> List[Rule]:
        models = self.session.query(RuleModel).filter(RuleModel.organization_id == org_id).all()
        return [RuleMapper.to_domain(m) for m in models]
    
    async def get_active_by_audit_type(self, org_id: UUID, audit_type: str) -> List[Rule]:
        models = self.session.query(RuleModel).filter(
            and_(
                RuleModel.organization_id == org_id,
                RuleModel.audit_type == audit_type,
                RuleModel.is_active == True
            )
        ).all()
        return [RuleMapper.to_domain(m) for m in models]
    
    async def update(self, rule: Rule) -> Rule:
        model = self.session.query(RuleModel).filter(RuleModel.id == rule.id).first()
        if model:
            model.name = rule.name
            model.conditions = rule.conditions
            model.severity = rule.severity.value
            model.is_active = rule.is_active
            model.updated_at = rule.updated_at
            self.session.commit()
            self.session.refresh(model)
        return RuleMapper.to_domain(model)
    
    async def delete(self, rule_id: UUID) -> bool:
        model = self.session.query(RuleModel).filter(RuleModel.id == rule_id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False


class SQLAlchemyFindingRepository(FindingRepository):
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, finding: Finding) -> Finding:
        model = FindingMapper.to_model(finding)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return FindingMapper.to_domain(model)
    
    async def get_by_id(self, finding_id: UUID) -> Optional[Finding]:
        model = self.session.query(FindingModel).filter(FindingModel.id == finding_id).first()
        return FindingMapper.to_domain(model) if model else None
    
    async def get_by_audit(self, audit_id: UUID) -> List[Finding]:
        models = self.session.query(FindingModel).filter(FindingModel.audit_id == audit_id).all()
        return [FindingMapper.to_domain(m) for m in models]
    
    async def get_by_severity(self, audit_id: UUID, severity: str) -> List[Finding]:
        models = self.session.query(FindingModel).filter(
            and_(
                FindingModel.audit_id == audit_id,
                FindingModel.severity == severity
            )
        ).all()
        return [FindingMapper.to_domain(m) for m in models]
    
    async def delete(self, finding_id: UUID) -> bool:
        model = self.session.query(FindingModel).filter(FindingModel.id == finding_id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False
    
    async def delete_by_audit(self, audit_id: UUID) -> int:
        count = self.session.query(FindingModel).filter(FindingModel.audit_id == audit_id).delete()
        self.session.commit()
        return count
