import pytest
from app.app import create_test_app

@pytest.fixture
def app():
    app = create_test_app()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()