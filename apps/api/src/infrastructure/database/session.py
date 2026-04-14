from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from infrastructure.database.config import DatabaseSettings

database_settings = DatabaseSettings()

engine = create_engine(database_settings.url, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
