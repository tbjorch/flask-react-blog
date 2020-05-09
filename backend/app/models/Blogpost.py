# 3rd party modules
from werkzeug.exceptions import BadRequest

# Internal modules
from app import db
from app.models.BaseModel import BaseModel


class Blogpost(BaseModel, db.Model):
    headline: str = db.Column(db.String(300), nullable=False)
    body: str = db.Column(db.Text, nullable=False)
    author_id: int = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False)

    def __init__(self, headline, body, user_id) -> None:
        if not isinstance(headline, str) and isinstance(body, str):
            raise BadRequest("Expected parameters to be strings")
        self.headline = headline
        self.body = body
        self.author_id = user_id
