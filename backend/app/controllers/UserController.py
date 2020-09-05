# Standard library
from typing import Dict, List

# 3rd party modules
from flask import Response
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized

# Internal modules
from app.controllers import BaseController, AuthController
from app.models import User, Role

auth = AuthController.get_instance()


class UserController(BaseController):

    def create_user(self) -> Response:
        data: Dict = self.get_required_data_from_request(
            "username", "password")
        user: User = User.find_by_username(data["username"])
        if user is not None:
            raise BadRequest("Username is already taken")
        new_user: User = User(
            data["username"],
            auth.create_pw_hash(data["password"]))
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

    def get_all(self) -> Response:
        users: List[User] = User.find_all()
        if users is None:
            raise NotFound("No users exist")
        user_json_list = [user.to_dict() for user in users]
        return self.make_json_response(user_json_list)

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
            raise Unauthorized("Username or password is incorrect")
        auth_dict = auth.authenticate(user.password_hash, data["password"])
        if auth_dict["is_authenticated"]:
            if auth_dict["new_pw_hash"] is not None:
                user.password_hash = auth_dict["new_pw_hash"]
                user.save()
            jwt_token: bytes = auth.create_jwt_token(
                user.id,
                user.username,
                [role.name for role in user.roles]
            )
            return self.make_json_response(
                {
                    "message": "User successfully authenticated!"
                }, token=jwt_token
            )
