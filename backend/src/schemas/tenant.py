from pydantic import BaseModel
from typing import List, Optional

class TenantBase(BaseModel):
    name: str

class TenantCreate(TenantBase):
    pass

class TenantUpdate(TenantBase):
    pass

class Tenant(TenantBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class TenantList(BaseModel):
    tenants: List[Tenant]