#!/usr/bin/env python3
"""
This module contains a class to manage the API authentication.
"""
from flask import request
from typing import List, TypeVar
import fnmatch
import os


class Auth:
    """
    Manages the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for the given path based on
        the excluded paths list.

        Args:
            path (str): The path to check.
            excluded_paths (list): The list of paths or patterns
                                   (with possible wildcards) that are excluded
                                   from requiring authentication.

        Returns:
            bool: True if authentication is required,
                  False if it's excluded by the patterns.
        """
        if path is None or excluded_paths is None:
            return True

        # Ensure path ends with a slash for comparison
        if not path.endswith('/'):
            path += '/'

        for pattern in excluded_paths:
            # Ensure excluded pattern has a trailing slash too
            if not pattern.endswith('/'):
                pattern += '/'
            if fnmatch.fnmatch(path, pattern):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns the authorization header """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user """
        return None

    def session_cookie(self, request=None):
        """
        Returns the value of the session cookie from a request.

        Args:
            request: The Flask request object.

        Returns:
            The value of the session cookie, or None if not found.
        """
        if request is None:
            return None

        # Retrieve the cookie name from the environment variable
        cookie_name = os.getenv("SESSION_NAME", "_my_session_id")

        # Get the cookie value
        return request.cookies.get(cookie_name)
