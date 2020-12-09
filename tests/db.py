from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def override_get_engine():
    return engine


def override_db_dependencies(app: FastAPI, engine: Engine):
    app.dependency_overrides[engine] = override_get_engine
