# Standard library
from typing import List

# 3rd party modules
from argon2 import PasswordHasher
from werkzeug.exceptions import Unauthorized

# Internal modules
from app.models import User


class AuthController:
    ph = PasswordHasher()

    def authenticate(self, user: User, password: str) -> None:
        pw_verified: bool = self.ph.verify(user.password_hash, password)
        if pw_verified and self.ph.check_needs_rehash(user.password_hash):
            user.password_hash = self.ph.hash(password)
            user.__save__()
        if not pw_verified:
            raise Unauthorized("User or password is incorrect")

    def create_pw_hash(self, password: str) -> str:
        return self.ph.hash(password)

    def authorize(user: User, roles: List[str]) -> bool:
        pass
