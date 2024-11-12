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
        # email, password = decoded_base64_authorization_header.split(":", 1)
        # return email, password

        # Split the string into email and password
        try:
            u_credentials = decoded_base64_authorization_header.split(":", 1)
            if len(u_credentials) != 2:
                return None, None

            user_email = u_credentials[0]
            user_pwd = u_credentials[1]
            return user_email, user_pwd
        except Exception:
            return None, None

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

        try:
            # Search for a user with the provided email
            users = User.search({'email': user_email})
            if not users:
                return None

            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance associated with the provided request.

        Args:
            request: Flask request object.

        Returns:
            User: The User instance if credentials are valid, otherwise None.
        """
        # Retrieve the Authorization header
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        # Extract and decode the Base64 part of the header
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None

        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None

        # Extract user credentials from decoded string
        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        if user_email is None or user_pwd is None:
            return None

        # Retrieve the user from the database
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
