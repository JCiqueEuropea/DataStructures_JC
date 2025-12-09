from sqlalchemy.orm import Session
from app.errors import EntityNotFoundError
from app.models import ProductResponse, ProductCreate
from app.models.sql_models import ProductSQL
from app.services.store_manager import store


class ProductService:
    @staticmethod
    def create(db: Session, product_in: ProductCreate) -> ProductResponse:

        db_product = ProductSQL(**product_in.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        response = ProductResponse.model_validate(db_product)

        store.insert_product(response)

        return response

    @staticmethod
    def get_by_id(db: Session, product_id: int) -> ProductResponse:
        product = store.find_product(product_id)
        if product:
            return product

        db_product = db.query(ProductSQL).filter(ProductSQL.id == product_id).first()

        if not db_product:
            raise EntityNotFoundError(entity="Product", identifier=str(product_id))

        response = ProductResponse.model_validate(db_product)
        store.insert_product(response)

        return response
