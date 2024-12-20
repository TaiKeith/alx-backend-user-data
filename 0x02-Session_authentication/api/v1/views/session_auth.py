#!/usr/bin/env python3
"""
This module contains views for Session authentication.
"""
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login/', methods=['POST'],
                 strict_slashes=False)
def login():
    """
    POST /auth_session/login:
        Handles user login by validating email and password,
        creates a session and returns user information in JSON.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve user by email
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            # Create session ID for the user
            session_id = auth.create_session(user.id)

            response = jsonify(user.to_json())
            session_name = os.getenv("SESSION_NAME")
            response.set_cookie(session_name, session_id)
            return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    DELETE /auth_session/logout:
        Logs out a user by destroying their session.
    """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
