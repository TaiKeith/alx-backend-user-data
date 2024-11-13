#!/usr/bin/env python3
"""
This module contains a class SessionAuth that inherits from Auth for
session authentication.
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    SessionAuth class for session-based authentication.
    """
    # Class attribute to store user_id by session_id
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a given user_id.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The created session ID, or None if user_id is invalid.
        """
        # Validate user_id
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a new session ID
        session_id = str(uuid.uuid4())

        # Store the session in the dictionary
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves a User ID based on a Session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The User ID associated with the session ID,
                 or None if invalid.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        # Retrieve the User ID from the dictionary
        return self.user_id_by_session_id.get(session_id)
