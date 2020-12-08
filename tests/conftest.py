from fastapi.testclient import TestClient
import pytest

from api import get_app


@pytest.fixture(scope='session')
def app():
    app = get_app()
    yield app


@pytest.fixture(scope='module')
def client(app):
    client = TestClient(app=app)
    yield client
