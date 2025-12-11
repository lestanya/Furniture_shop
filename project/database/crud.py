from typing import List, Optional
from sqlalchemy.orm import Session

from .models import Product, DepartmentWorkTime, Department


# CRUD операции  (ПРОДУКТЫ)

def get_all_products(db: Session) -> List[Product]:
    return db.query(Product).all()


def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(
    db: Session,
    *,
    product_type: str,
    product_name: str,
    material_type: str,
    article: str | None = None,
    min_partner_cost: float | None = None,
) -> Product:
    product = Product(
        product_type=product_type,
        product_name=product_name,
        material_type=material_type,
        article=article,
        min_partner_cost=min_partner_cost,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(
    db: Session,
    product_id: int,
    *,
    product_type: str,
    product_name: str,
    material_type: str,
    article: str | None = None,
    min_partner_cost: float | None = None,
) -> Optional[Product]:
    product = get_product(db, product_id)
    if not product:
        return None

    product.product_type = product_type
    product.product_name = product_name
    product.material_type = material_type
    product.article = article
    product.min_partner_cost = min_partner_cost

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> bool:
    product = get_product(db, product_id)
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True




def get_workshops_for_product(db: Session, product_id: int):
    """
    Возвращает список цехов для продукта с временем производства.
    """
    rows = (
        db.query(DepartmentWorkTime, Department)
        .join(Department, DepartmentWorkTime.department_id == Department.id)
        .filter(DepartmentWorkTime.product_id == product_id)
        .all()
    )

    result = []
    for wt, dept in rows:
        result.append(
            {
                "department_id": dept.id,
                "department_name": dept.department_name,
                "department_type": dept.department_type,
                "production_time": float(wt.production_time),
                "workers_count": len(dept.workers) if dept.workers else 0,
            }
        )
    return result
