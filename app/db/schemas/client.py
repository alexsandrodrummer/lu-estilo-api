from pydantic import BaseModel, EmailStr, constr

class ClientBase(BaseModel):
    nome: str
    email: EmailStr
    cpf: constr
    telefone: str | None = None
    endereco: str | None = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class ClientOut(ClientBase):
    id: int

    class Config:
        orm_mode = True
