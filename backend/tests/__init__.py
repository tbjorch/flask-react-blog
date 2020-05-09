from app import app, db


class CustomTestClient:
    def __init__(self):
        self.test_client = app.test_client()

    def __enter__(self):
        db.create_all()
        return self.test_client

    def __exit__(self, exc_type, exc_val, exc_tb):
        db.drop_all()
