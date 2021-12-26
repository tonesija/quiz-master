from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_database_url

engine = create_engine(get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Used as a dependency for routers.

    Yields:
        (SessionLocal): database session.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
