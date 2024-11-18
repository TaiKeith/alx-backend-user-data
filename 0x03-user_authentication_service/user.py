#!/usr/bin/env python3
"""
This module contains an SQLAlchemy model named `User` for a database table
named `users` by using the mapping declaration of SQLAlchemy.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """
    Represents a user in the database.

    Attributes:
        id (int): The primary key of the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        session_id (str | None): The session ID of the user.
        reset_token (str | None): The token used for resetting the user's
                                  password.
    """
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: str | None = Column(String(250), nullable=True)
    reset_token: str | None = Column(String(250), nullable=True)

    def __repr__(self) -> str:
        """
        Returns a string representation of the User instance.

        Returns:
            str: A string showing the user's ID and email.
        """
        return f"<User(id={self.id}, email='{self.email}')>"

