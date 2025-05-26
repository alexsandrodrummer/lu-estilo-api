from pydantic import BaseModel
from datetime import datetime

class OrderBase(BaseModel):
    cliente_id: int
    status: str = "pendente"
    produtos: list[int]

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: str

class OrderOut(OrderBase):
    id: int
    data_criacao: datetime

    class Config:
        orm_mode = True
