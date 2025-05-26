from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.db import models, schemas
from app.db.session import SessionLocal
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.order.OrderOut)
def create_order(order: schemas.order.OrderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    produtos = db.query(models.product.Product).filter(models.product.Product.id.in_(order.produtos)).all()

    if not produtos:
        raise HTTPException(status_code=400, detail="Produtos inválidos")

    for produto in produtos:
        if produto.estoque <= 0:
            raise HTTPException(status_code=400, detail=f"Produto {produto.id} sem estoque")
        produto.estoque -= 1

    db_order = models.order.Order(cliente_id=order.cliente_id)
    db_order.produtos = produtos

    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/", response_model=List[schemas.order.OrderOut])
def get_orders(
    db: Session = Depends(get_db),
    periodo: str = Query(None),
    secao: str = Query(None),
    id_pedido: int = Query(None),
    status: str = Query(None),
    cliente: int = Query(None),
    skip: int = 0,
    limit: int = 10,
    user=Depends(get_current_user)
):
    query = db.query(models.order.Order)
    if id_pedido:
        query = query.filter(models.order.Order.id == id_pedido)
    if status:
        query = query.filter(models.order.Order.status == status)
    if cliente:
        query = query.filter(models.order.Order.cliente_id == cliente)
    return query.offset(skip).limit(limit).all()

@router.get("/{id}", response_model=schemas.order.OrderOut)
def get_order(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    order = db.query(models.order.Order).get(id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order

@router.put("/{id}", response_model=schemas.order.OrderOut)
def update_order(id: int, order: schemas.order.OrderUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_order = db.query(models.order.Order).get(id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    db_order.status = order.status
    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/{id}")
def delete_order(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_order = db.query(models.order.Order).get(id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    db.delete(db_order)
    db.commit()
    return {"msg": "Pedido excluído"}
