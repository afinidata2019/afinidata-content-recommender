from fastapi.testclient import TestClient
import pytest

from api import get_app
from api.core.db import get_db, get_engine
from tests.db import override_db_dependencies


@pytest.fixture(scope='session')
def app():
    app = get_app()
    yield app


@pytest.fixture(scope='session', autouse=True)
def overrride_database(app):
    override_db_dependencies(app, get_db, get_engine)


@pytest.fixture(scope='module')
def client(app):
    client = TestClient(app=app)
    yield client
