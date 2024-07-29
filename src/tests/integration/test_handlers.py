import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.service import app


@pytest.fixture
def client():
    """Тестовый клиент."""
    return TestClient(app)


def test_root(client):
    """Тестирует корень."""
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'server is running'}
