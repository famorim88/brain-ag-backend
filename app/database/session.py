# backend/app/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import DATABASE_URL

# Cria o motor (engine) do SQLAlchemy.
# connect_args={"check_same_thread": False} é geralmente para SQLite,
# mas não faz mal em PostgreSQL. Pode ser removido se não for usado.
engine = create_engine(DATABASE_URL)

# Cria uma sessão local do banco de dados.
# autocommit=False: Não comita automaticamente após cada operação.
# autoflush=False: Não salva automaticamente as alterações pendentes no banco.
# bind=engine: Conecta a sessão ao motor do banco de dados.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declaração base para os modelos SQLAlchemy.
# Todos os modelos da sua aplicação herdarão desta classe.
Base = declarative_base()

# Função de dependência para obter uma sessão do banco de dados.
# Esta função será usada pelo FastAPI para injetar a sessão
# nas rotas que precisam interagir com o banco de dados.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()