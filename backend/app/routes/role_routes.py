# 3rd party modules
from flask import Response

# Internal modules
from app import app
from app.controllers import RoleController


controller = RoleController()


@app.route("/roles", methods=["POST"])
def create_role() -> Response:
    return controller.create_role()


@app.route("/roles/<id>", methods=["GET"])
def find_role_by_id(id: int) -> Response:
    return controller.find_role_by_id(id)


@app.route("/roles", methods=["GET"])
def find_role_by_name() -> Response:
    return controller.find_role_by_name()


@app.route("/roles/<id>", methods=["DELETE"])
def delete_role_by_id(id: int) -> Response:
    return controller.delete_role(id)
