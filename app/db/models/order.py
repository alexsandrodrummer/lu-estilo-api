from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Table
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime

order_product = Table(
    'order_product', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clients.id'))
    status = Column(String, default='pendente')
    data_criacao = Column(DateTime, default=datetime.utcnow)

    produtos = relationship("Product", secondary=order_product)
