from pydantic import BaseModel, Field
from typing import Optional, List


class ProductBase(BaseModel):
    product_type: str
    product_name: str
    material_type: str
    article: Optional[str] = None
    min_partner_cost: Optional[float] = Field(default=None, ge=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True


class WorkshopOut(BaseModel):
    department_id: int
    department_name: str
    department_type: str
    workers_count: int
    production_time: float


class TimeOut(BaseModel):
    product_id: int
    hours: int


class RawMaterialRequest(BaseModel):
    product_type: str
    material_type: str
    quantity: int
    param1: float
    param2: float


class RawMaterialOut(BaseModel):
    amount: int
