from fastapi.testclient import TestClient
import pytest
import uuid

from ugeougeo.main import app


@pytest.fixture()
def client():
    """FastAPI client instance."""
    return TestClient(app)


@pytest.fixture()
def email():
    u = uuid.uuid4().hex[:6]
    return u + '@gmail.com'


@pytest.fixture()
def password():
    return uuid.uuid4().hex[:10]


@pytest.fixture()
def nickname():
    return uuid.uuid4().hex[:10]


@pytest.fixture()
def username():
    return uuid.uuid4().hex[:10]
