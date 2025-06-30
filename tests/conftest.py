import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.main import app
from app.database.base import Base # Para criar tabelas de teste
from app.database.session import get_db # Para sobrescrever a dependência

# SQLite in-memory para testes rápidos e isolados
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    """Cria e retorna o motor do banco de dados de teste."""
    # Cria todas as tabelas para o banco de dados de teste
    Base.metadata.create_all(bind=engine)
    yield engine
    # Opcional: drop_all() para limpar o banco de dados após a sessão de testes
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    """Retorna uma sessão de banco de dados nova e limpa para cada teste."""
    connection = db_engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)

    # Sobrescreve o get_db para usar a sessão de teste
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db

    yield db

    # Rollback na transação para limpar o banco de dados após cada teste
    transaction.rollback()
    connection.close()
    app.dependency_overrides = {} # Limpa as sobrescritas após o teste

@pytest.fixture(scope="module")
def client(db_session): # A fixture 'db_session' será executada antes de 'client'
    """Retorna um cliente de teste para a aplicação FastAPI."""
    with TestClient(app) as c:
        yield c