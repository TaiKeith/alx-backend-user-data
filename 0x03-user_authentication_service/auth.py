#!/usr/bin/env python3
"""
This module contains a method _hash_password that takes in a password as
a string and returns bytes.
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hashes a password with a salted hash using bcrypt.

    Args:
        password (str): The password to hash.
    Returns:
        bytes: The salted hash of the password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the provided email and password.

        Args:
            email (str): The email of the user to register.
            password (str): The plain-text password of the user.
        Returns:
            User: The created User object.
        Raises:
            ValueError: If a user with the same email already exists.
        """
        try:
            # Check if the user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # User doesn't exist; proceed to create one
            hashed = _hash_password(password)
            new_user = self._db.add_user(email, hashed)  # Create the user
            return new_user
