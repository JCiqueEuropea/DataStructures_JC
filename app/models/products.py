from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict


class ProductBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Commercial name of the product"
    )

    price: float = Field(
        ...,
        gt=0,
        description="Price must be greater than 0"
    )

    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Brief product description"
    )

    @field_validator('name')
    @classmethod
    def name_must_be_title_case(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('Name cannot be empty or whitespace only')
        return v.title()

    @field_validator('price')
    @classmethod
    def round_price(cls, v: float) -> float:
        return round(v, 2)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
