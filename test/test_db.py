import os
import unittest
from sqlalchemy import text

from app import create_app
from app.db import db


class ConnectionTestCase(unittest.TestCase):
    def setUp(self):
        # Asegura entorno de testing y evita leer .env
        os.environ["FLASK_CONTEXT"] = "testing"
        os.environ["FLASK_SKIP_DOTENV"] = "1"
        os.environ["SECRET_KEY"] = "test-secret-key"
        os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_db_connection(self):
        # Verificación simple y portable (sirve en SQLite)
        value = db.session.execute(text("SELECT 1")).scalar()
        self.assertEqual(value, 1)
