from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import os

from .config import settings
from .database import get_db, engine, Base
from .models import User, Organization, Audit, Rule, Finding, AuditType, AuditStatus
from .schemas import (
    UserCreate, UserLogin, TokenResponse, UserResponse,
    OrganizationCreate, OrganizationResponse, OrganizationListResponse,
    AuditResponse, AuditListResponse, AuditDetailResponse,
    RuleCreate, RuleUpdate, RuleResponse, RuleListResponse,
    FindingListResponse
)
from .utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)

# Create tables
Base.metadata.create_all(bind=engine)

# Create uploads directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-tenant AI Cloud Cost & Multi-Niche Auditor API",
    version=settings.APP_VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Dependency to get current user
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user = db.query(User).filter(User.id == payload["sub"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


# ============================================================================
# HEALTH & ROOT ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.post("/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    new_user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate tokens
    access_token = create_access_token({"sub": str(new_user.id)})
    refresh_token = create_access_token({"sub": str(new_user.id)}, expires_days=7)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.from_orm(new_user)
    )

@app.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Generate tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_access_token({"sub": str(user.id)}, expires_days=7)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.from_orm(user)
    )

@app.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.from_orm(current_user)


# ============================================================================
# ORGANIZATION ENDPOINTS
# ============================================================================

@app.post("/organizations", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org_data: OrganizationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_org = Organization(
        name=org_data.name,
        owner_id=current_user.id
    )
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    
    return OrganizationResponse.from_orm(new_org)

@app.get("/organizations", response_model=OrganizationListResponse)
async def list_organizations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orgs = db.query(Organization).filter(Organization.owner_id == current_user.id).all()
    return OrganizationListResponse(
        organizations=[OrganizationResponse.from_orm(org) for org in orgs],
        total=len(orgs)
    )

@app.get("/organizations/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    org = db.query(Organization).filter(
        Organization.id == org_id,
        Organization.owner_id == current_user.id
    ).first()
    
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    
    return OrganizationResponse.from_orm(org)


# ============================================================================
# AUDIT ENDPOINTS
# ============================================================================

@app.post("/audits/upload", response_model=AuditResponse, status_code=status.HTTP_201_CREATED)
async def upload_audit(
    organization_id: UUID = Form(...),
    audit_type: AuditType = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify organization ownership
    org = db.query(Organization).filter(
        Organization.id == organization_id,
        Organization.owner_id == current_user.id
    ).first()
    
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    
    # Validate file
    if not file.filename.endswith(tuple(settings.ALLOWED_EXTENSIONS)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed: {settings.ALLOWED_EXTENSIONS}"
        )
    
    # Save file
    file_path = os.path.join(settings.UPLOAD_DIR, f"{org.id}_{file.filename}")
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Create audit
    new_audit = Audit(
        organization_id=organization_id,
        audit_type=audit_type,
        file_name=file.filename,
        file_path=file_path,
        created_by=current_user.id,
        status=AuditStatus.PENDING
    )
    db.add(new_audit)
    db.commit()
    db.refresh(new_audit)
    
    # TODO: Trigger async processing of audit
    
    return AuditResponse.from_orm(new_audit)

@app.get("/audits", response_model=AuditListResponse)
async def list_audits(
    organization_id: Optional[UUID] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Audit).join(Organization).filter(
        Organization.owner_id == current_user.id
    )
    
    if organization_id:
        query = query.filter(Audit.organization_id == organization_id)
    
    audits = query.order_by(Audit.created_at.desc()).all()
    
    return AuditListResponse(
        audits=[AuditResponse.from_orm(audit) for audit in audits],
        total=len(audits)
    )

@app.get("/audits/{audit_id}", response_model=AuditDetailResponse)
async def get_audit(
    audit_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    audit = db.query(Audit).join(Organization).filter(
        Audit.id == audit_id,
        Organization.owner_id == current_user.id
    ).first()
    
    if not audit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit not found")
    
    findings_count = db.query(Finding).filter(Finding.audit_id == audit_id).count()
    
    response = AuditDetailResponse.from_orm(audit)
    response.findings_count = findings_count
    
    return response

@app.get("/audits/{audit_id}/findings", response_model=FindingListResponse)
async def get_audit_findings(
    audit_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify access
    audit = db.query(Audit).join(Organization).filter(
        Audit.id == audit_id,
        Organization.owner_id == current_user.id
    ).first()
    
    if not audit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit not found")
    
    findings = db.query(Finding).filter(Finding.audit_id == audit_id).all()
    
    return FindingListResponse(
        findings=[FindingResponse.from_orm(f) for f in findings],
        total=len(findings)
    )


# ============================================================================
# RULE ENDPOINTS
# ============================================================================

@app.post("/rules", response_model=RuleResponse, status_code=status.HTTP_201_CREATED)
async def create_rule(
    rule_data: RuleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify organization ownership
    org = db.query(Organization).filter(
        Organization.id == rule_data.organization_id,
        Organization.owner_id == current_user.id
    ).first()
    
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    
    new_rule = Rule(
        organization_id=rule_data.organization_id,
        name=rule_data.name,
        description=rule_data.description,
        audit_type=rule_data.audit_type,
        conditions=rule_data.conditions,
        severity=rule_data.severity,
        is_active=rule_data.is_active,
        created_by=current_user.id
    )
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    
    return RuleResponse.from_orm(new_rule)

@app.get("/rules", response_model=RuleListResponse)
async def list_rules(
    organization_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify organization ownership
    org = db.query(Organization).filter(
        Organization.id == organization_id,
        Organization.owner_id == current_user.id
    ).first()
    
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    
    rules = db.query(Rule).filter(Rule.organization_id == organization_id).all()
    
    return RuleListResponse(
        rules=[RuleResponse.from_orm(rule) for rule in rules],
        total=len(rules)
    )

@app.put("/rules/{rule_id}", response_model=RuleResponse)
async def update_rule(
    rule_id: UUID,
    rule_data: RuleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rule = db.query(Rule).join(Organization).filter(
        Rule.id == rule_id,
        Organization.owner_id == current_user.id
    ).first()
    
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")
    
    for key, value in rule_data.dict(exclude_unset=True).items():
        setattr(rule, key, value)
    
    db.commit()
    db.refresh(rule)
    
    return RuleResponse.from_orm(rule)

@app.delete("/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(
    rule_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rule = db.query(Rule).join(Organization).filter(
        Rule.id == rule_id,
        Organization.owner_id == current_user.id
    ).first()
    
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")
    
    db.delete(rule)
    db.commit()
    
    return None


# ============================================================================
# DASHBOARD ENDPOINTS
# ============================================================================

@app.get("/dashboard/metrics")
async def get_dashboard_metrics(
    organization_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify organization ownership
    org = db.query(Organization).filter(
        Organization.id == organization_id,
        Organization.owner_id == current_user.id
    ).first()
    
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    
    # Get metrics
    total_audits = db.query(Audit).filter(Audit.organization_id == organization_id).count()
    completed_audits = db.query(Audit).filter(
        Audit.organization_id == organization_id,
        Audit.status == AuditStatus.COMPLETED
    ).count()
    
    total_findings = db.query(Finding).join(Audit).filter(
        Audit.organization_id == organization_id
    ).count()
    
    # Calculate average optimization score
    audits_with_scores = db.query(Audit).filter(
        Audit.organization_id == organization_id,
        Audit.optimization_score.isnot(None)
    ).all()
    
    avg_score = None
    if audits_with_scores:
        avg_score = sum(a.optimization_score for a in audits_with_scores) / len(audits_with_scores)
    
    return {
        "total_audits": total_audits,
        "completed_audits": completed_audits,
        "total_findings": total_findings,
        "avg_optimization_score": avg_score,
        "active_rules": db.query(Rule).filter(
            Rule.organization_id == organization_id,
            Rule.is_active == True
        ).count()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
