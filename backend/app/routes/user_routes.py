# 3rd party modules
from flask import Response

# Internal modules
from app import app
from app.controllers import UserController, AuthController

controller: UserController = UserController()
auth = AuthController.get_instance()


@app.route('/api/v1/users', methods=['POST'])
def create_user() -> Response:
    return controller.create_user()


@app.route('/api/v1/users/<id>', methods=['GET'])
def find_user(id) -> Response:
    return controller.find_by_id(id)


@app.route('/api/v1/users', methods=['GET'])
@auth.authorize(["ADMIN"])
def find_all_users() -> Response:
    return controller.get_all()


@app.route('/api/v1/users/<id>', methods=['DELETE'])
@auth.authorize(["ADMIN"])
def delete_user(id) -> Response:
    return controller.delete_user(id)


@app.route('/api/v1/users/<id>/roles', methods=['POST'])
@auth.authorize(["ADMIN"])
def add_role(id) -> Response:
    return controller.add_role(id)


@app.route('/api/v1/users/<id>/roles', methods=['DELETE'])
@auth.authorize(["ADMIN"])
def delete_role(id) -> Response:
    return controller.delete_role(id)


@app.route('/api/v1/login', methods=['POST'])
def login() -> Response:
    return controller.login()
