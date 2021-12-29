import os
from fastapi.testclient import TestClient
from pydantic.tools import T
import pytest
from contextlib import contextmanager
from sqlalchemy.orm.session import sessionmaker
from main import app
from sqlalchemy import create_engine
from db.db import Base, SessionLocal, get_db
from config import get_database_url

# Database for UTs should end in _test.
DATABASE_URL = f"{get_database_url()}_test"

engine = create_engine(DATABASE_URL)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Setups a clean db for every test case."""

    drop_db_tables(engine)
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = get_test_db
    yield  # Run tests
    drop_db_tables(engine)


def get_test_db():
    """Mock for fastapi app's get_db dependancy."""

    SessionLocal = sessionmaker(bind=engine)
    test_db = SessionLocal()

    try:
        yield test_db
    finally:
        test_db.close()


def drop_db_tables(engine):
    """Drop tables from the db.

    Args:
        engine ([type]): [description]
    """

    Base.metadata.drop_all(bind=engine, tables=reversed(Base.metadata.sorted_tables))


def delete_db_data(db):
    """Deletes all date from the db.

    Args:
        db ([type]): [description]
    """

    for tbl in reversed(Base.metadata.sorted_tables):
        db.execute(tbl.delete())


@contextmanager
def test_db_session():
    """Session for usage outside of routes."""

    SessionLocal = sessionmaker(bind=engine)
    test_db = SessionLocal()

    try:
        yield test_db
    finally:
        test_db.close()


@pytest.fixture
def fixture_db_session():
    """Yields session, after test tears down everything."""

    SessionLocal = sessionmaker(bind=engine)
    test_db = SessionLocal()

    yield test_db

    delete_db_data(test_db)

    test_db.commit()
    test_db.close()


@pytest.fixture
def client():
    """Yields fastapi test client."""

    with TestClient(app) as client:
        yield client
