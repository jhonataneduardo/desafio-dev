import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.database.session import Base, get_db
from main import app
from fastapi.testclient import TestClient

TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def test_engine():
    """Cria um engine SQLite por teste."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},  # necessário para SQLite
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_session(test_engine):
    """Cria uma sessão de banco de dados para testes."""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def client(test_session):
    """TestClient com override de get_db para usar SQLite in-memory."""

    def override_get_db():
        try:
            yield test_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def cnab_valid_file_content() -> bytes:
    """Conteúdo de arquivo CNAB válido para testes de integração."""
    line1 = b"3201903010000014200096206760174753****3153153453JOAO MACEDO   BAR DO JOAO CENTRO"
    line2 = b"5201903010000013200556418150633123****7687145607MARIA JOSEFINALOJA DO O - CENTRO"
    return line1 + b"\n" + line2
