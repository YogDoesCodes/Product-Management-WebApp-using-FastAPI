from fastapi import FastAPI, Depends
from database import engine, Base
from models import Product
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import ProductCreate
from typing import List
from schemas import Product_Response


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message":"Product API Running!"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products", response_model=Product_Response)
def create_products(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name = product.name,
        price = product.price,
        quantity = product.quantity
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products", response_model=List[Product_Response])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@app.put("/products/{product_id}", response_model=Product_Response)
def update_product(
    product_id: int,
    updated_product: ProductCreate,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return {"error": "Product not found"}

    product.name = updated_product.name
    product.price = updated_product.price
    product.quantity = updated_product.quantity

    db.commit()
    db.refresh(product)

    return product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return {"error": "Product not found"}

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}






