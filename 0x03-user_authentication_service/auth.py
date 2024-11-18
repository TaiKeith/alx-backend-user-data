#!/usr/bin/env python3
"""
This module contains a method _hash_password that takes in a password as
a string and returns bytes.
"""
import bcrypt

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
