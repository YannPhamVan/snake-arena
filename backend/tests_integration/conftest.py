"""
Integration test configuration for Snake Arena backend.

Integration tests use a real SQLite database file (not in-memory) to test
end-to-end functionality including database persistence, API endpoints,
and authentication flows.
"""

import pytest
import os
import tempfile
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app as fastapi_app
from app.database import Base, get_db
import app.db_models  # noqa: F401


@pytest.fixture(scope="module")
def test_db_file():
    """Create a temporary database file for integration tests"""
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield db_path
    # Cleanup after all tests in module
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture(scope="module")
def engine(test_db_file):
    """Create SQLAlchemy engine with test database"""
    database_url = f"sqlite:///{test_db_file}"
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="module")
def SessionLocal(engine):
    """Create session factory"""
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session(SessionLocal):
    """Create a fresh database session for each test"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """Create a test client with database dependency override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    fastapi_app.dependency_overrides[get_db] = override_get_db
    yield TestClient(fastapi_app)
    fastapi_app.dependency_overrides.clear()
