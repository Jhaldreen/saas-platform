from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, Enum as SQLEnum, Text, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owned_organizations = relationship("OrganizationModel", back_populates="owner", foreign_keys="OrganizationModel.owner_id")
    audits = relationship("AuditModel", back_populates="created_by_user")


class OrganizationModel(Base):
    __tablename__ = 'organizations'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner = relationship("UserModel", back_populates="owned_organizations", foreign_keys=[owner_id])
    audits = relationship("AuditModel", back_populates="organization")
    rules = relationship("RuleModel", back_populates="organization")


class AuditModel(Base):
    __tablename__ = 'audits'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=False)
    audit_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    status = Column(String, nullable=False)
    total_cost_or_revenue = Column(Float, nullable=True)
    optimization_score = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    organization = relationship("OrganizationModel", back_populates="audits")
    created_by_user = relationship("UserModel", back_populates="audits")
    findings = relationship("FindingModel", back_populates="audit")


class RuleModel(Base):
    __tablename__ = 'rules'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    audit_type = Column(String, nullable=False)
    conditions = Column(JSON, nullable=False)
    severity = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    organization = relationship("OrganizationModel", back_populates="rules")
    findings = relationship("FindingModel", back_populates="rule")


class FindingModel(Base):
    __tablename__ = 'findings'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_id = Column(UUID(as_uuid=True), ForeignKey('audits.id'), nullable=False)
    rule_id = Column(UUID(as_uuid=True), ForeignKey('rules.id'), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String, nullable=False)
    cost_impact = Column(Float, nullable=True)
    evidence = Column(JSON, nullable=True)
    recommendation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    audit = relationship("AuditModel", back_populates="findings")
    rule = relationship("RuleModel", back_populates="findings")
