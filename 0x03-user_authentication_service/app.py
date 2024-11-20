#!/usr/bin/env python3
"""
This module contains a basic Flask app setup.
"""
from flask import Flask, jsonify, request, abort, redirect

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


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout() -> None:
    """
    Log out a user by destroying their session.

    Returns:
        JSON response with a message indicating logout success.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None or session_id is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    Fetch user profile using the session_id cookie.

    Returns:
        JSON response with the user's email if the session is valid.
        Responds with 403 if the session is invalid or user does not exist.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None or not session_id:
        abort(403)

    return jsonify({"email": f"{user.email}"}), 200


@app.route('/reset_password', methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Handles the eset password request by generating a reset token.

    Returns:
        JSON response with the user's email and the reset token or 403 error.
    """
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route('/reset_password', methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    Handles the password update request.

    Returns:
        JSON response confirming the update or raises a 403 error.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": f"{email}", "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
