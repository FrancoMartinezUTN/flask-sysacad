import os
import unittest

from flask import current_app

from app import create_app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        # Configurar entorno para testing sin depender de .env
        os.environ['FLASK_CONTEXT'] = 'testing'
        os.environ['FLASK_SKIP_DOTENV'] = '1'
        
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
        # Limpiar env vars de testing
        for var in ('FLASK_CONTEXT', 'FLASK_SKIP_DOTENV'):
            os.environ.pop(var, None)

    def test_app(self):
        """Verifica que la app se crea correctamente y current_app existe."""
        self.assertIsNotNone(current_app)


if __name__ == '__main__':
    unittest.main()
