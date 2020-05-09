# Standard library
from typing import Dict

# 3rd party modules
from flask import Response
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized

# Internal modules
from app.controllers import BaseController, AuthController
from app.models import User, Role


class UserController(BaseController):

    ac: AuthController = AuthController()

    def create_user(self) -> Response:
        data: Dict = self.get_required_data_from_request(
            "username", "password")
        user: User = User.find_by_username(data["username"])
        if user is not None:
            raise BadRequest("Username is already taken")
        new_user: User = User(
            data["username"],
            self.ac.create_pw_hash(data["password"]))
        new_user.save()
        return self.make_json_response(
            dict(message="User successfully created")
            )

    def add_role(self, id) -> Response:
        data: Dict = self.get_required_data_from_request("role")
        user: User = User.find_by_id(id)
        if user is None:
            raise NotFound(f"No user found with id={id}")
        role: Role = Role.find_by_name(data["role"])
        if role is None:
            raise NotFound(f"No role found with name={data['role']}")
        user.roles.append(role)
        user.save()
        return self.make_json_response(
            dict(message="Role successfully added to user")
        )

    def delete_role(self, id) -> Response:
        data: Dict = self.get_required_data_from_request("role")
        user: User = User.find_by_id(id)
        if user is None:
            raise NotFound(f"No user found with id={id}")
        role: Role = Role.find_by_name(data["role"])
        if role is None:
            raise NotFound(f"No role found with name={data['role']}")
        user.roles.remove(role)
        user.save()
        return self.make_json_response(
            dict(message="Role successfully deleted from user")
        )

    def find_by_id(self, id) -> Response:
        user: User = User.find_by_id(id)
        if user is None:
            raise NotFound(f"No user found with id={id}")
        return self.make_json_response(user.to_dict())

    def find_by_username(self) -> Response:
        data: Dict = self.get_required_params_from_request("username")
        username: str = data["username"]
        user: User = User.find_by_username(username)
        if user is None:
            raise NotFound(f"No user found with username={data['username']}")
        return self.make_json_response(user.__to_dict__())

    def delete_user(self, id) -> Response:
        user: User = User.find_by_id(id)
        if user is None:
            raise NotFound(f"No user found with id={id}")
        user.delete()
        return self.make_json_response(
            {"message": "User successfully deleted"})

    def login(self) -> Response:
        data: Dict = \
            self.get_required_data_from_request("username", "password")
        user: User = User.find_by_username(data["username"])
        if user is None:
            raise Unauthorized("User or password is incorrect")
        self.ac.authenticate(user, data["password"])
        return self.make_json_response(
            {"message": "User successfully authenticated!"}
            )
