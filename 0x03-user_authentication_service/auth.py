#!/usr/bin/env python3
"""
This module contains methods and a class for handling user authentication.
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

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
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a uuid and returns its string representation.
    """
    return str(uuid4())


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
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login credentials.

        Args:
            email (str): user's email address.
            password (str): user's password.
        Return:
            bool: True if credentials are correct, else False.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """
        Creates a session ID for a user identified by email.

        Args:
            email (str): The email of the user.
        Returns:
            str: The new session ID, or None if the user does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()

        # Update the user's session_id in the database
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Takes a session_id and returns the corresponding user.

        Args:
            session_id (str): The session id for user.
        Return:
            user object if found, else None.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Take a user_id and destroy that user's session and update their
        session_id attribute to None.

        Args:
            user_id (int): The user's id.
        Return:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None

        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset_token uuid for a user identified by the given email.

        Args:
            email (str): The user's email address.
        Return:
            newly generated reset_token for the relevant user.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user's password using the provided reset_token.

        Args:
            reset_token (str): Token used to authenticate the password reset.
            password (str): The new password to set for the user.

        Raises:
            ValueError: If the reset_token is invalid or does not exist.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed, reset_token=None)
