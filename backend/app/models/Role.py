# Internal modules
from app import db
from app.models.BaseModel import BaseModel
from app.models.User import user_role


class Role(BaseModel, db.Model):
    name: str = db.Column(db.String(50), unique=True, nullable=False)
    description: str = db.Column(db.Text, nullable=True)
    users = db.relationship('User', secondary=user_role, lazy=True)

    def __init__(self, name, description) -> None:
        self.name = name
        self.description = description

    @staticmethod
    def find_by_name(name):
        return Role.query.filter_by(name=name).first()
