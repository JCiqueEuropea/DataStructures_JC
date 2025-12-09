from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ProductResponse, ProductCreate
from app.services import ProductService
from app.services import get_api_key

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[Depends(get_api_key)]
)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
        product: ProductCreate,
        db: Session = Depends(get_db)
):
    """
    Creates a new product in SQL Server and adds it to the BST in memory.
    """
    return ProductService.create(db, product)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
        product_id: int,
        db: Session = Depends(get_db)
):
    """
    Retrieves a product. Checks memory (BST) first, then SQL Server.
    Time Complexity: O(log n) if cached, else SQL Query time.
    """
    return ProductService.get_by_id(db, product_id)
