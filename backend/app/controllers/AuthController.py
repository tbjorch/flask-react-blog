# Standard library
from typing import List, Dict
from datetime import datetime, timedelta
from functools import wraps

# 3rd party modules
from argon2 import PasswordHasher
from werkzeug.exceptions import Unauthorized
import jwt
from flask import request

# Internal modules
# from app.models import User


class AuthController:
    instance = None

    @staticmethod
    def get_instance():
        if AuthController.instance is None:
            AuthController.instance = AuthController()
        return AuthController.instance

    def __init__(self):
        self.SECRET = "ABC123"
        self.ph = PasswordHasher()

    def authenticate(self, pw_hash: str, password: str) -> Dict:
        pw_verified: bool = self.ph.verify(pw_hash, password)
        new_pw_hash = None
        if pw_verified and self.ph.check_needs_rehash(pw_hash):
            new_pw_hash = self.ph.hash(password)
        if not pw_verified:
            raise Unauthorized("User or password is incorrect")
        return {'new_pw_hash': new_pw_hash, 'is_authenticated': True}

    def create_pw_hash(self, password: str) -> str:
        return self.ph.hash(password)

    def authorize(self, authorized_roles: List[str]):
        def decorated_function(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                self._has_authorized_roles(authorized_roles)
                return function(*args, **kwargs)
            return wrapper
        return decorated_function

    def _has_authorized_roles(self, authorized_roles: List[str]):
        # Check that auth cookie exist in request
        try:
            token = request.cookies.get("Authorization")
        except KeyError:
            raise Unauthorized("You need to be logged in")
        # Try to decode cookie to ensure user is authenticated
        user_data = self.decode_jwt_token(token)
        if (len(authorized_roles) == 0):
            return
        try:
            for role in authorized_roles:
                if role in user_data["roles"]:
                    return
            raise Unauthorized(
                        "You are not authorized to perform this action"
                        )
        except KeyError:
            raise Unauthorized(
                "You don't have permission to perform this action")

    def create_jwt_token(
            self,
            user_id: int,
            username: str,
            roles: List = None) -> bytes:
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(hours=3),
                'iat': datetime.utcnow(),
                'sub': dict(user_id=user_id, username=username, roles=roles),
            }
            return jwt.encode(
                payload,
                self.SECRET,
                algorithm='HS256'
            )
        except Exception as e:
            print(e)

    def decode_jwt_token(self, jwt_token: bytes) -> Dict:
        if jwt_token is None:
            raise Unauthorized("You need to be signed in")
        try:
            payload = jwt.decode(jwt_token, self.SECRET, algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Token has expired, please sign in again")
        except jwt.InvalidTokenError:
            raise Unauthorized("Token is invalid, please sign in again")
