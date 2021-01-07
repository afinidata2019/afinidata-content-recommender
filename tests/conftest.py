from fastapi.testclient import TestClient
import pytest
from sqlalchemy import text

from api import get_app
from api.core.db import get_engine
from tests.db import override_db_dependencies, override_get_engine


@pytest.fixture(scope='session')
def app():
    app = get_app()
    yield app


@pytest.fixture(scope='session', autouse=True)
def overrride_database(app):
    override_db_dependencies(app, get_engine)
