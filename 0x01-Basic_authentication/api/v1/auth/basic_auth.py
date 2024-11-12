#!/usr/bin/env python3
"""
This module contains a BacicAuth class that inherits from Auth.
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ BasicAuth class that inherits from Auth. """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic
        Authentication.

        Args:
            authorization_header (str): The Authorization header from
                                        the request.

        Returns:
            str: The Base64 part of the Authorization header,
                 or None if invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        # Return the portion after "Basic "
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64 string and returns the UTF-8 string value.

        Args:
            base64_authorization_header (str): The Base64 string to decode.

        Returns:
            str: The decoded string in UTF-8, or None if decoding fails.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts the user email and password from the decoded Base64
        authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded Base64
                                                       string.

        Returns:
            tuple: (user_email, user_password) if valid,
                   otherwise (None, None).
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split on the first occurrence of ':' to get email and password
        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieves a User instance based on the provided email and password.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            User: The User instance if credentials are valid, otherwise None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for a user with the provided email
        users = User.search({'email': user_email})
        if not users:
            return None

        user = users[0]
        # Validate the password using User's is_valid_password method
        if not user.is_valid_password(user_pwd):
            return None

        return user
