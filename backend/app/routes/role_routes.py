# 3rd party modules
from flask import Response

# Internal modules
from app import app
from app.controllers.RoleController import RoleController
from app.controllers.AuthController import AuthController


controller = RoleController()
auth = AuthController.get_instance()


@app.route("/api/v1/roles", methods=["POST"])
@auth.authorize(["ADMIN"])
def create_role() -> Response:
    return controller.create_role()


@app.route("/api/v1/roles/<id>", methods=["GET"])
@auth.authorize(["ADMIN"])
def find_role_by_id(id: int) -> Response:
    return controller.find_role_by_id(id)


@app.route("/api/v1/roles", methods=["GET"])
@auth.authorize(["ADMIN"])
def find_role_by_name() -> Response:
    return controller.find_role_by_name()


@app.route("/api/v1/roles/<id>", methods=["DELETE"])
@auth.authorize(["ADMIN"])
def delete_role_by_id(id: int) -> Response:
    return controller.delete_role(id)
