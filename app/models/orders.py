from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict


class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0, description="Valid Product ID")
    quantity: int = Field(..., gt=0, le=100, description="Quantity must be between 1 and 100")


class OrderItemResponse(OrderItemCreate):
    pass


class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(
        ...,
        min_length=1,
        description="Order must contain at least one item"
    )

    @field_validator('items')
    @classmethod
    def validate_unique_products(cls, v: List[OrderItemCreate]) -> List[OrderItemCreate]:
        product_ids = [item.product_id for item in v]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError('Duplicate products found in order. Please consolidate quantities.')
        return v


class OrderUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(Pending|Shipped|Delivered|Cancelled)$")
    items: Optional[List[OrderItemCreate]] = Field(None, min_length=1)

    @field_validator('items')
    @classmethod
    def validate_unique_products_update(cls, v: Optional[List[OrderItemCreate]]) -> Optional[List[OrderItemCreate]]:
        if v is None: return v
        product_ids = [item.product_id for item in v]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError('Duplicate products found in order update.')
        return v


class OrderResponse(BaseModel):
    id: int
    status: str
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)
