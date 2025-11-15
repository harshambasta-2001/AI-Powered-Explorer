import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root to the path to resolve import errors
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from app.database import Base, DBFactory
from app.config import settings
from app.models.user import User
from app.utils.helper_functions import hash

# Use a separate database for testing
TEST_DATABASE_URL = settings.DATABASE_URL + "_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create and tear down the test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Provide a transactional scope around a test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Provide a test client for the app."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    # Override the dependency
    app.dependency_overrides[DBFactory] = override_get_db

    with TestClient(app) as c:
        yield c

    # Clean up dependency overrides
    app.dependency_overrides.clear()