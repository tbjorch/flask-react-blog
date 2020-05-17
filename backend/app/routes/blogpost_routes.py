# 3rd party modules
from flask import Response

# Internal modules
from app import app
from app.controllers import BlogpostController, AuthController

controller: BlogpostController = BlogpostController()
auth = AuthController.get_instance()


@app.route('/')
def hello_world() -> Response:
    return "Hello world!"


@app.route('/blogposts', methods=['POST'])
def create_blogpost() -> Response:
    return controller.create_blogpost()


@app.route('/blogposts', methods=['GET'])
def find_all() -> Response:
    return controller.find_all()


@app.route('/blogposts/<id>', methods=['GET'])
def find_blogpost(id) -> Response:
    return controller.find_by_id(id)


@app.route('/blogposts/<id>', methods=['DELETE'])
@auth.authorize(["ADMIN"])
def delete_blogpost(id) -> Response:
    return controller.delete_blogpost(id)
