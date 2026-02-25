from app.main import app
from app.db import Base, get_db
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pytest
from dotenv import load_dotenv
import os
import sys

# Это должно быть ПЕРВЫМ — до любых импортов из app
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

load_dotenv(os.getenv("ENV_FILE", ".env"))


TEST_DATABASE_URL = os.environ["TEST_DATABASE_URL"]

test_engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True, future=True)
TestSessionLocal = sessionmaker(
    bind=test_engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def db():
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
