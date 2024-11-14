#!/usr/bin/env python3
"""
This module contains SessionDBAuth class for managing session IDs stored
in the database.
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from flask import request

class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth extends SessionExpAuth to store sessions in a database.
    """
    def create_session(self, user_id=None):
        """
        Create a session for a user, saving it in the database.
        Args:
            user_id (str): The user's ID
        Returns:
            session_id (str): The created session ID, or None if creation failed.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Create and save the session to the database
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve a user ID based on a session ID stored in the database.
        Args:
            session_id (str): The session ID
        Returns:
            user_id (str): The ID of the user associated with the session ID, or None.
        """
        user_id = UserSession.search({"session_id": session_id})
        if user_id:
            return user_id
        return None

    def destroy_session(self, request=None):
        """
        Destroys the user session based on the session cookie from the request.
        Args:
            request (flask.Request): The incoming request
        Returns:
            bool: True if the session was successfully destroyed, False otherwise.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Find and delete the session from the database
        sessions = UserSession.search({"session_id": session_id})
        if not sessions:
            return False

        user_session = sessions[0]
        user_session.remove()
        return True
