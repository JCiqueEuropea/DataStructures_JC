from typing import List, Optional

from sqlalchemy.orm import Session

from app.errors import EntityNotFoundError, BusinessRuleError
from app.models import OrderCreate, OrderResponse
from app.models.orders import OrderUpdate, OrderItemResponse
from app.models.sql_models import OrderSQL, OrderItemSQL
from app.services.product_service import ProductService
from app.services.store_manager import store


class OrderService:

    @staticmethod
    def create(db: Session, order_in: OrderCreate) -> OrderResponse:
        for item in order_in.items:
            try:
                ProductService.get_by_id(db, item.product_id)
            except EntityNotFoundError:
                raise BusinessRuleError(
                    message=f"Product with ID {item.product_id} does not exist. Cannot create order."
                )

        db_order = OrderSQL(status="Pending")
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        for item in order_in.items:
            db_item = OrderItemSQL(
                order_id=db_order.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            db.add(db_item)

        db.commit()
        db.refresh(db_order)

        response = OrderService._map_to_response(db_order)
        store.add_order(response)

        return response

    @staticmethod
    def get_by_id(db: Session, order_id: int) -> OrderResponse:
        order = store.get_order(order_id)
        if order:
            return order

        db_order = OrderService._get_order_sql_or_404(db, order_id)

        response = OrderService._map_to_response(db_order)
        store.add_order(response)

        return response

    @staticmethod
    def get_all(db: Session) -> List[OrderResponse]:
        if not store.orders_head:
            db_orders: List[OrderSQL] = db.query(OrderSQL).all()

            for db_o in db_orders:
                response = OrderService._map_to_response(db_o)
                store.add_order(response)

        return store.get_all_orders()

    @staticmethod
    def update(db: Session, order_id: int, order_update: OrderUpdate) -> OrderResponse:
        db_order = OrderService._get_order_sql_or_404(db, order_id)

        if order_update.status:
            db_order.status = order_update.status

        if order_update.items is not None:
            for item in order_update.items:
                try:
                    ProductService.get_by_id(db, item.product_id)
                except EntityNotFoundError:
                    raise BusinessRuleError(f"Product ID {item.product_id} invalid.")

            db.query(OrderItemSQL).filter(OrderItemSQL.order_id == order_id).delete()

            for item in order_update.items:
                new_db_item = OrderItemSQL(
                    order_id=order_id,
                    product_id=item.product_id,
                    quantity=item.quantity
                )
                db.add(new_db_item)

        db.commit()
        db.refresh(db_order)

        response = OrderService._map_to_response(db_order)
        store.add_order(response)

        return response

    @staticmethod
    def delete(db: Session, order_id: int):
        store.remove_order(order_id)

        db_order = OrderService._get_order_sql_or_404(db, order_id)

        db.delete(db_order)
        db.commit()

    @staticmethod
    def _get_order_sql_or_404(db: Session, order_id: int) -> OrderSQL:
        db_order: Optional[OrderSQL] = db.query(OrderSQL).filter(OrderSQL.id == order_id).first()

        if not db_order:
            raise EntityNotFoundError(entity="Order", identifier=str(order_id))
        return db_order

    @staticmethod
    def _map_to_response(db_order: OrderSQL) -> OrderResponse:
        sql_items = list(db_order.items) if db_order.items else []

        items_pydantic = [
            OrderItemResponse(product_id=i.product_id, quantity=i.quantity)
            for i in sql_items
        ]

        return OrderResponse(
            id=int(db_order.id),
            status=str(db_order.status),
            items=items_pydantic
        )
