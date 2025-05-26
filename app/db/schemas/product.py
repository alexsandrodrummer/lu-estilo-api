from pydantic import BaseModel, constr, condecimal
from datetime import date

class ProductBase(BaseModel):
    descricao: str
    valor_venda: condecimal(gt=0)
    codigo_barras: str
    secao: str | None = None
    estoque: int
    validade: date | None = None
    imagens: list[str] = []

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
