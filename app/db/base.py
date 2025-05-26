from app.db.models import user, client, product, order  # Importa todos os modelos
from app.db.session import Base
from sqlalchemy.orm import declarative_base

Base = declarative_base()