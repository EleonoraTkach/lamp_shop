from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from models import Product, Category
from db import get_db

router = APIRouter(prefix="/api/v1")


# 📦 PRODUCTS

@router.get("/products/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id, Product.is_deleted == False).first()
    if not product:
        raise HTTPException(404, "Product not found")
    return product


@router.patch("/products/{id}")
def update_product(id: int, data: dict, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id, Product.is_deleted == False).first()
    if not product:
        raise HTTPException(404, "Product not found")

    for key, value in data.items():
        setattr(product, key, value)

    product.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(product)
    return product


@router.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    product.is_deleted = True
    db.commit()
    return {"status": "deleted"}


# 📂 CATEGORY → PRODUCTS

@router.get("/categories/{id}/products")
def get_category_products(id: int, db: Session = Depends(get_db)):
    return db.query(Product).filter(
        Product.category_id == id,
        Product.is_deleted == False
    ).all()


@router.post("/categories/{id}/products")
def create_product(id: int, data: dict, db: Session = Depends(get_db)):
    product = Product(**data, category_id=id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


# 📂 CATEGORIES

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).filter(Category.is_deleted == False).all()


@router.post("/categories")
def create_category(data: dict, db: Session = Depends(get_db)):
    category = Category(**data)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/categories/{id}")
def update_category(id: int, data: dict, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == id, Category.is_deleted == False).first()
    if not category:
        raise HTTPException(404, "Category not found")

    for key, value in data.items():
        setattr(category, key, value)

    category.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(category)
    return category


@router.delete("/categories/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(404, "Category not found")

    category.is_deleted = True
    db.commit()
    return {"status": "deleted"}