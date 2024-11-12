#!/usr/bin/env python3
"""
This module contains a class to manage the API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Manages the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if authentication is required """
        if path not in excluded_paths and path is None:
            return True

    def authorization_header(self, request=None) -> str:
        """ Returns the authorization header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user """
        return None
