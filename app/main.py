from fastapi import FastAPI
from app.api.routes import auth, clients, products, orders
from app.core.config import settings
from app.core.middleware import add_exception_handler
from app.api import dependencies
from app.db.session import SessionLocal
add_exception_handler


app = FastAPI(
    title="Lu Estilo API",
    description="API RESTful para a loja Lu Estilo",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(products.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "Bem-vindo à API Lu Estilo"}
