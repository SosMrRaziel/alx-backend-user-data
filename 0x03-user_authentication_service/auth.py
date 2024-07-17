#!/usr/bin/env python3
""" Auth module """
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Returns a salted, hashed password """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
