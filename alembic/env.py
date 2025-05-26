from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
from app.db.base import Base  
from app.core.config import settings

# Configuração do Alembic
config = context.config

# Adicione esta linha no seu env.py
target_metadata = Base.metadata
target_metadata.schema = 'lu_estilo_schema'  # Usa o novo schema

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Interpretar config file para loggers
fileConfig(config.config_file_name)

# Troca automática de URL assíncrona para síncrona
DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL.startswith("postgresql+asyncpg"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg", "postgresql")

config.set_main_option('sqlalchemy.url', DATABASE_URL)

# Modelos a serem mapeados
target_metadata = Base.metadata

def run_migrations_offline():
    """Rodar migrações no modo offline."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Rodar migrações no modo online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
