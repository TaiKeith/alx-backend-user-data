#!/usr/bin/env python3
"""
This module contains a class to manage the API authentication.
"""
from flask import request
from typing import List, TypeVar
import fnmatch


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

        for pattern in excluded_paths:
            if fnmatch.fnmatch(path, pattern):
                return False
        return True

        # Ensure path ends with a slash for comparison
        # if not path.endswith('/'):
        # path += '/'

        # Check if the normalized path is in excluded_paths
        # return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """ Returns the authorization header """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user """
        return None
