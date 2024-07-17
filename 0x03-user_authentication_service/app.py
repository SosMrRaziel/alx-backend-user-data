#!/usr/bin/env python3
""" Main file """
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome():
    """ Welcome message """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run()
