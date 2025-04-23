from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


# Base Product Schema
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    sku: str
    category: str
    subcategory: Optional[str] = None
    base_price: float = Field(..., gt=0)
    is_active: bool = True


# Schema for creating a product
class ProductCreate(ProductBase):
    pass


# Schema for updating a product
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    base_price: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None


# Schema for returning a product
class ProductResponse(ProductBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Schema for product list
class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int


# Base Price Schema
class PriceBase(BaseModel):
    price_value: float = Field(..., gt=0)
    price_date: datetime
    is_promotional: bool = False


# Schema for creating a price
class PriceCreate(PriceBase):
    product_id: str


# Schema for updating a price
class PriceUpdate(BaseModel):
    price_value: Optional[float] = Field(None, gt=0)
    price_date: Optional[datetime] = None
    is_promotional: Optional[bool] = None


# Schema for returning a price
class PriceResponse(PriceBase):
    id: str
    product_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Schema for returning prices with pagination
class PriceListResponse(BaseModel):
    items: List[PriceResponse]
    total: int
