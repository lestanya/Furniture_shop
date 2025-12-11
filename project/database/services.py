from sqlalchemy.orm import Session

from .models import DepartmentWorkTime, ProductCoefficient, LoseCoefficient
from .models import Product, Department  # если нужно


class ManufacturingService:
    @staticmethod
    def calculate_manufacturing_time(product_id: int, db: Session) -> int:
        """
        Суммируем время по всем DepartmentWorkTime для продукта.
        Если нет записей — возвращаем -1.
        """
        rows = (
            db.query(DepartmentWorkTime)
            .filter(DepartmentWorkTime.product_id == product_id)
            .all()
        )
        if not rows:
            return -1

        total = sum(float(r.production_time) for r in rows)
        if total < 0:
            return -1
        return int(round(total))

    @staticmethod
    def calculate_required_materials(
        product_type: str,
        material_type: str,
        quantity: int,
        param1: float,
        param2: float,
        db: Session,
    ) -> int:
        """
        Пример реализации метода по ТЗ (использует ProductCoefficient и LoseCoefficient).
        Если данных нет или параметры некорректны — возвращает -1.
        """
        if quantity <= 0 or param1 <= 0 or param2 <= 0:
            return -1

        coeff_row = (
            db.query(ProductCoefficient)
            .join(Product, ProductCoefficient.product_id == Product.id)
            .filter(Product.product_type == product_type)
            .first()
        )
        if not coeff_row:
            return -1

        lose_row = (
            db.query(LoseCoefficient)
            .filter(LoseCoefficient.material_type == material_type)
            .first()
        )
        if not lose_row:
            return -1

        product_coeff = float(coeff_row.coefficient)
        loss_percent = float(lose_row.lose_percentage)

        raw_per_unit = param1 * param2 * product_coeff
        total_raw = quantity * raw_per_unit
        total_with_loss = total_raw * (1 + loss_percent / 100.0)

        if total_with_loss < 0:
            return -1
        return int(round(total_with_loss))
