from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.core.config import get_settings


settings = get_settings()

DB_URI = settings.DB_URI
engine = create_engine(DB_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_engine():
    return engine
