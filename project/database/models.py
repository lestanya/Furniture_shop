# models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DECIMAL,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    product_type = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    article = Column(String, unique=True)
    min_partner_cost = Column(DECIMAL(10, 2))
    material_type = Column(String, nullable=False)

    coefficient = relationship(
        "ProductCoefficient",
        back_populates="product",
        uselist=False,
    )
    work_times = relationship("DepartmentWorkTime", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.product_name}')>"


class ProductCoefficient(Base):
    __tablename__ = "product_coefficient"

    id = Column(Integer, primary_key=True)
    product_id = Column(
        Integer,
        ForeignKey("product.id"),
        unique=True,
        nullable=False,
    )
    coefficient = Column(DECIMAL(5, 3), nullable=False)

    product = relationship("Product", back_populates="coefficient")

    def __repr__(self):
        return (
            f"<ProductCoefficient(product_id={self.product_id}, "
            f"coeff={self.coefficient})>"
        )


class LoseCoefficient(Base):
    __tablename__ = "lose_coefficient"

    id = Column(Integer, primary_key=True)
    material_type = Column(String, unique=True, nullable=False)
    lose_percentage = Column(DECIMAL(5, 2), nullable=False)

    def __repr__(self):
        return (
            f"<LoseCoefficient(material='{self.material_type}', "
            f"lose={self.lose_percentage}%)>"
        )


class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True)
    department_name = Column(String, unique=True, nullable=False)
    department_type = Column(String, nullable=False)

    workers = relationship("DepartmentWorkers", back_populates="department")
    work_times = relationship("DepartmentWorkTime", back_populates="department")

    def __repr__(self):
        return f"<Department(id={self.id}, name='{self.department_name}')>"


class DepartmentWorkers(Base):
    __tablename__ = "department_workers"

    id = Column(Integer, primary_key=True)
    department_id = Column(
        Integer,
        ForeignKey("department.id"),
        nullable=False,
    )
    workers_count = Column(Integer, nullable=False)

    department = relationship("Department", back_populates="workers")

    def __repr__(self):
        return (
            f"<DepartmentWorkers(department_id={self.department_id}, "
            f"workers={self.workers_count})>"
        )


class DepartmentWorkTime(Base):
    __tablename__ = "department_work_time"

    id = Column(Integer, primary_key=True)

    product_id = Column(
        Integer,
        ForeignKey("product.id"),
        nullable=False,
    )
    department_id = Column(
        Integer,
        ForeignKey("department.id"),
        nullable=False,
    )

 
    department_name = Column(String, nullable=False)
    production_time = Column(DECIMAL(8, 2), nullable=False)

    product = relationship("Product", back_populates="work_times")
    department = relationship("Department", back_populates="work_times")

    def __repr__(self):
        return (
            f"<DepartmentWorkTime(product={self.product_id}, "
            f"dept='{self.department_name}', time={self.production_time})>"
        )
