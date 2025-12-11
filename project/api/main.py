from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connect_db import init_db, get_db
from database import crud
from database.services import ManufacturingService
from .schemas import (
    ProductCreate,
    ProductUpdate,
    ProductOut,
    WorkshopOut,
    TimeOut,
    RawMaterialRequest,
    RawMaterialOut,
)

app = FastAPI(
    title="Furniture Company Management System",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/ping")
def ping():
    return {"status": "ok"}


# ПРОДУКТЫ

@app.get("/api/products", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    products = crud.get_all_products(db)
    return products


@app.get("/api/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/api/products", response_model=ProductOut, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    product = crud.create_product(
        db,
        product_type=data.product_type,
        product_name=data.product_name,
        material_type=data.material_type,
        article=data.article,
        min_partner_cost=data.min_partner_cost,
    )
    return product


@app.put("/api/products/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
):
    product = crud.update_product(
        db,
        product_id,
        product_type=data.product_type,
        product_name=data.product_name,
        material_type=data.material_type,
        article=data.article,
        min_partner_cost=data.min_partner_cost,
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.delete("/api/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_product(db, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")


# ЦЕХИ

@app.get(
    "/api/products/{product_id}/workshops",
    response_model=list[WorkshopOut],
)
def product_workshops(product_id: int, db: Session = Depends(get_db)):
    workshops = crud.get_workshops_for_product(db, product_id)
    if not workshops:
        raise HTTPException(status_code=404, detail="No workshops for product")
    return workshops


# ВРЕМЯ ЦЕХОВ

@app.get(
    "/api/products/{product_id}/time",
    response_model=TimeOut,
)
def product_time(product_id: int, db: Session = Depends(get_db)):
    hours = ManufacturingService.calculate_manufacturing_time(product_id, db)
    if hours < 0:
        raise HTTPException(status_code=404, detail="Product or workshops not found")
    return TimeOut(product_id=product_id, hours=hours)


# ПОДСЧЕТ

@app.post("/api/raw-material", response_model=RawMaterialOut)
def calc_raw_material(payload: RawMaterialRequest, db: Session = Depends(get_db)):
    amount = ManufacturingService.calculate_required_materials(
        product_type=payload.product_type,
        material_type=payload.material_type,
        quantity=payload.quantity,
        param1=payload.param1,
        param2=payload.param2,
        db=db,
    )
    if amount < 0:
        raise HTTPException(status_code=400, detail="Invalid input data")
    return RawMaterialOut(amount=amount)
