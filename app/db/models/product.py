from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from app.db.session import Base

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    valor_venda = Column(Float, nullable=False)
    codigo_barras = Column(String, unique=True, index=True, nullable=False)
    secao = Column(String)
    estoque = Column(Integer, default=0)
    validade = Column(Date, nullable=True)
    imagens = Column(String)  # URLs separadas por vírgula
