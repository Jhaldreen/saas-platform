from sqlalchemy.orm import Session
from models.tenant import Tenant
from schemas.tenant import TenantCreate, TenantUpdate

class TenantService:
    def __init__(self, db: Session):
        self.db = db

    def create_tenant(self, tenant_data: TenantCreate) -> Tenant:
        new_tenant = Tenant(**tenant_data.dict())
        self.db.add(new_tenant)
        self.db.commit()
        self.db.refresh(new_tenant)
        return new_tenant

    def get_tenant(self, tenant_id: int) -> Tenant:
        return self.db.query(Tenant).filter(Tenant.id == tenant_id).first()

    def update_tenant(self, tenant_id: int, tenant_data: TenantUpdate) -> Tenant:
        tenant = self.get_tenant(tenant_id)
        if tenant:
            for key, value in tenant_data.dict(exclude_unset=True).items():
                setattr(tenant, key, value)
            self.db.commit()
            self.db.refresh(tenant)
        return tenant

    def delete_tenant(self, tenant_id: int) -> bool:
        tenant = self.get_tenant(tenant_id)
        if tenant:
            self.db.delete(tenant)
            self.db.commit()
            return True
        return False

    def get_all_tenants(self) -> list[Tenant]:
        return self.db.query(Tenant).all()