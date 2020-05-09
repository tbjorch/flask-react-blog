# Standard library
from typing import Dict

# 3rd party modules
from flask import Response
from werkzeug.exceptions import NotFound, BadRequest

# Internal modules
from app.controllers.BaseController import BaseController
from app.models import Role


class RoleController(BaseController):

    def create_role(self) -> Response:
        req_data: Dict = \
            self.get_required_data_from_request("name", "description")
        if Role.find_by_name(req_data["name"]) is not None:
            raise BadRequest("Role with provided name already exists")
        role: Role = Role(req_data["name"], req_data["description"])
        role.save()
        return self.make_json_response(
            dict(
                message="Role successfully created"
            )
        )

    def find_role_by_id(self, id) -> Response:
        role: Role = Role.find_by_id(id)
        if role is None:
            raise NotFound("No role found with provided id")
        return self.make_json_response(
            role.to_dict()
        )

    def find_role_by_name(self) -> Response:
        req_data: Dict = self.get_required_params_from_request("name")
        role: Role = Role.find_by_name(req_data["name"])
        if role is None:
            raise NotFound("No role found with provided name")
        return self.make_json_response(
            role.to_dict()
        )

    def delete_role(self, id) -> Response:
        role: Role = Role.find_by_id(id)
        if role is None:
            raise NotFound("No role found with provided id")
        role.delete()
        return self.make_json_response(
            dict(
                message="Role successfully deleted"
            )
        )
