#!/usr/bin/env python3
"""A Flask app"""

from flask import Flask, jsonify, request

from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """Index route"""

    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """Route to register a new user"""

    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": f"{email}", "message": "user created"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
