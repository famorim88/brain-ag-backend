from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
import os
import sys
from alembic import context
# Carregar variáveis de ambiente do .env
from dotenv import load_dotenv
load_dotenv()
from app.core.config import DATABASE_URL
from app.database.session import Base # Importa a Base que seus modelos herdam
# ADICIONE ESTA(S) LINHA(S) PARA IMPORTAR SEUS MODELOS!
import app.models.producer # <--- SEUS MODELOS ESTÃO EM producer.py
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
sys.path.append(os.path.abspath("."))
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    sqlalchemy_url_config = {
        "sqlalchemy.url": DATABASE_URL # Aqui está a correção!
    }
    connectable = engine_from_config(
        sqlalchemy_url_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
