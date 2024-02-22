#!/usr/bin/env python3
"""auth.py module"""

import bcrypt
import logging
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

from db import DB
from user import User


logging.disable(logging.WARNING)


def _hash_password(password: str) -> bytes:
    """Hashes a user's input password"""

    hashed_p = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hashed_p


def _generate_uuid() -> str:
    """Returns a string representation of a new uuid"""

    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user into the database"""

        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_p = _hash_password(password)
            user = self._db.add_user(email, hashed_p)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks for valid user credentials"""

        try:
            user = self._db.find_user_by(email=email)
            if user:
                if bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password
                ):
                    return True
        except NoResultFound:
            return False

        return False
