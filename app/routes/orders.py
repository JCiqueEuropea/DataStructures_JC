from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import OrderResponse, OrderCreate
from app.models.orders import OrderUpdate
from app.services import OrderService
from app.services import get_api_key

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    dependencies=[Depends(get_api_key)]
)


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
        order: OrderCreate,
        db: Session = Depends(get_db)
):
    """
    Creates a new order.
    Validates business rules (e.g., product existence) before creation.
    """
    return OrderService.create(db, order)


@router.get("/", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    """
    Lists all active orders. Loads from SQL if memory is empty (Cold Start).
    """
    return OrderService.get_all(db)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
        order_id: int,
        db: Session = Depends(get_db)
):
    """
    Retrieves a specific order by ID checking Memory then SQL.
    """
    return OrderService.get_by_id(db, order_id)


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
        order_id: int,
        order_update: OrderUpdate,
        db: Session = Depends(get_db)
):
    """
    Updates an existing order (Status or Items).
    Updates SQL Server and syncs the changes to the Linked List in memory.
    """
    return OrderService.update(db, order_id, order_update)


@router.delete("/{order_id}", status_code=status.HTTP_200_OK)
def delete_order(
        order_id: int,
        db: Session = Depends(get_db)
):
    """
    Deletes an order from both memory (Linked List) and SQL Server.
    """
    OrderService.delete(db, order_id)
    return {"detail": "Order deleted successfully"}
