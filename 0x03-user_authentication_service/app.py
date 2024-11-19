#!/usr/bin/env python3
"""
This module contains a basic Flask app setup.
"""
from flask import Flask, jsonify, request, abort

from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    Returns a JSON response.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"], strict_slashes=False)
def users() -> str:
    """
    Registers new users
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": f"{email}", "message": "user created"})


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    Login user and create a new session.

    Returns:
        - 401 status code if login information is incorrect.
        - JSON response with a session cookie if login succeeds.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    # Validate login credentials
    if not AUTH.valid_login(email, password):
        abort(401)

    # Create a session for the user
    session_id = AUTH.create_session(email)

    # Create the response object
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
