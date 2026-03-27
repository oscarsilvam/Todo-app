import pytest
import sys
from pathlib import Path

# Add parent directory to path so we can import app and models_data
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from models_data import db

@pytest.fixture()
def app():
    test_app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with test_app.app_context(): 
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()
        db.session.remove()
        db.drop_all()   


@pytest.fixture()
def client(app):
    return app.test_client()        