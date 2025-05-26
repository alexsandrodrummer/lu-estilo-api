from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import models, schemas
from app.db.session import SessionLocal
from typing import List
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/clients", tags=["clients"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.client.ClientOut)
def create_client(client: schemas.client.ClientCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if db.query(models.client.Client).filter(models.client.Client.email == client.email).first():
        raise HTTPException(status_code=400, detail="Email já registrado")
    if db.query(models.client.Client).filter(models.client.Client.cpf == client.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já registrado")
    
    db_client = models.client.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/", response_model=List[schemas.client.ClientOut])
def get_clients(
    db: Session = Depends(get_db),
    nome: str = Query(None),
    email: str = Query(None),
    skip: int = 0,
    limit: int = 10,
    user=Depends(get_current_user)
):
    query = db.query(models.client.Client)
    if nome:
        query = query.filter(models.client.Client.nome.ilike(f"%{nome}%"))
    if email:
        query = query.filter(models.client.Client.email.ilike(f"%{email}%"))
    return query.offset(skip).limit(limit).all()

@router.get("/{id}", response_model=schemas.client.ClientOut)
def get_client(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    client = db.query(models.client.Client).get(id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client

@router.put("/{id}", response_model=schemas.client.ClientOut)
def update_client(id: int, client: schemas.client.ClientUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_client = db.query(models.client.Client).get(id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    for k, v in client.dict().items():
        setattr(db_client, k, v)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.delete("/{id}")
def delete_client(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_client = db.query(models.client.Client).get(id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(db_client)
    db.commit()
    return {"msg": "Cliente excluído"}
