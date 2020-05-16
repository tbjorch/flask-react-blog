# Standard library
from typing import List, Dict
from datetime import datetime, timedelta

# 3rd party modules
from argon2 import PasswordHasher
from werkzeug.exceptions import Unauthorized
import jwt

# Internal modules
from app.models import User


class AuthController:
    SECRET = "ABC123"
    ph = PasswordHasher()

    def authenticate(self, user: User, password: str) -> bytes:
        pw_verified: bool = self.ph.verify(user.password_hash, password)
        if pw_verified and self.ph.check_needs_rehash(user.password_hash):
            user.password_hash = self.ph.hash(password)
            user.__save__()
        if not pw_verified:
            raise Unauthorized("User or password is incorrect")
        return self.create_jwt_token(user.id, user.username, user.roles)

    def create_pw_hash(self, password: str) -> str:
        return self.ph.hash(password)

    def authorize(user: User, roles: List[str]) -> bool:
        pass

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
        try:
            payload = jwt.decode(jwt_token, self.SECRET, algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Token has expired, please sign in again")
        except jwt.InvalidTokenError:
            raise Unauthorized("Token is invalid, please sign in again")
