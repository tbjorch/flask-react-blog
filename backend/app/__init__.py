# Standard library
import json

# 3rd party modules
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from app import routes  # must be imported after app instantiation


@app.errorhandler(HTTPException)
def exception_handler(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "message": e.description,
    })
    response.content_type = "application/json"
    return response
