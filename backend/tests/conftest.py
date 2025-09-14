# backend/tests/conftest.py
import pytest
from app import create_app, db as app_db

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    # Use sqlite in-memory DB for fast tests
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        app_db.create_all()
        yield app
        app_db.session.remove()
        app_db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

