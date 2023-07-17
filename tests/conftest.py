import random

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


@pytest.fixture()
def price():
    return random.randint(1, 2147483647)


@pytest.fixture()
def price2():
    return random.randint(1, 2147483647)


@pytest.fixture()
def article():
    return uuid.uuid4().hex[:random.randint(1, 255)]


@pytest.fixture()
def article2():
    return uuid.uuid4().hex[:random.randint(1, 255)]
