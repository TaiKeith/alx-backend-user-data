#!/usr/bin/env python3
"""
This module contains UserSession model for storing session data in the
database.
"""
from models.base import Base


class UserSession(Base):
    """
    UserSession class to manage session persistence.
    Attributes:
        user_id (str): The ID of the user
        session_id (str): The session ID
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize UserSession with user_id and session_id
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
