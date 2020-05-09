# 3rd party modules
from flask import Response

# Internal modules
from app import app
from app.controllers import UserController

controller: UserController = UserController()


@app.route('/users', methods=['POST'])
def create_user() -> Response:
    return controller.create_user()


@app.route('/users/<id>', methods=['GET'])
def find_user(id) -> Response:
    return controller.find_by_id(id)


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id) -> Response:
    return controller.delete_user(id)


@app.route('/users/<id>/role', methods=['POST'])
def add_role(id) -> Response:
    return controller.add_role(id)


@app.route('/users/<id>/role', methods=['DELETE'])
def delete_role(id) -> Response:
    return controller.delete_role(id)


@app.route('/login', methods=['POST'])
def login() -> Response:
    return controller.login()
