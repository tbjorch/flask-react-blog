# 3rd party modules
from werkzeug.exceptions import BadRequest

# Internal modules
from app import db
from app.models.BaseModel import BaseModel


user_role = db.Table(
    'UserRole',
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True),
    db.Column(
        'role_id',
        db.Integer,
        db.ForeignKey('role.id'),
        primary_key=True)
)


class User(BaseModel, db.Model):
    username: str = db.Column(db.String(50), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(300), nullable=False)
    roles = db.relationship('Role', secondary=user_role, lazy=True)
    blogposts = db.relationship(
        'Blogpost',
        backref=db.backref('user', lazy=True)
        )

    def __init__(self, username, password_hash) -> None:
        if not isinstance(username, str) and isinstance(password_hash, str):
            raise BadRequest("Expected parameters to be strings")
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()
