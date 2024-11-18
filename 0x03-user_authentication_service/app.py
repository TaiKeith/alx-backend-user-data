#!/usr/bin/env python3
"""
This module contains a basic Flask app setup.
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    Returns a JSON response.
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
