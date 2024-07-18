#!/usr/bin/env python3
""" Main file """
from flask import Flask, jsonify, request, abort, redirect, make_response
from auth import Auth, _generate_uuid


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome():
    """ Welcome message """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ register user """
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        # Register user
        user = AUTH.register_user(email, password)

        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ login user """
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)
    if valid_login:
        # Create session
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ logout user """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/', code=302)  # Redirect to GET /
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def get_profile() -> str:

    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ get_reset_password_token """
    try:
        email = request.form.get('email')
        user = AUTH.get_user_from_email(email)
        if user:
            rest_token = AUTH.get_reset_password_token(email)
            return jsonify({"email": email, "reset_token": rest_token}), 200
        else:
            abort (403)
    except ValueError:
        rest_token = None


if __name__ == "__main__":
    app.run()
