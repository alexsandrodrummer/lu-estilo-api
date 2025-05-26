from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.db import models, schemas
from app.db.session import SessionLocal
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/products", tags=["products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.product.ProductOut)
def create_product(product: schemas.product.ProductCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_product = models.product.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=List[schemas.product.ProductOut])
def get_products(
    db: Session = Depends(get_db),
    categoria: str = Query(None),
    preco: float = Query(None),
    disponivel: bool = Query(None),
    skip: int = 0,
    limit: int = 10,
    user=Depends(get_current_user)
):
    query = db.query(models.product.Product)
    if categoria:
        query = query.filter(models.product.Product.secao.ilike(f"%{categoria}%"))
    if preco:
        query = query.filter(models.product.Product.valor_venda <= preco)
    if disponivel is not None:
        query = query.filter(models.product.Product.estoque > 0) if disponivel else query.filter(models.product.Product.estoque <= 0)
    return query.offset(skip).limit(limit).all()

@router.get("/{id}", response_model=schemas.product.ProductOut)
def get_product(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    product = db.query(models.product.Product).get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.put("/{id}", response_model=schemas.product.ProductOut)
def update_product(id: int, product: schemas.product.ProductUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_product = db.query(models.product.Product).get(id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for k, v in product.dict().items():
        setattr(db_product, k, v)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_product = db.query(models.product.Product).get(id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(db_product)
    db.commit()
    return {"msg": "Produto excluído"}
