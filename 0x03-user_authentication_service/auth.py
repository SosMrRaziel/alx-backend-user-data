#!/usr/bin/env python3
""" Auth module """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ Returns a salted, hashed password """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def _generate_uuid() -> str:
    """ Returns a string representation of a new UUID """
    new_uuid = str(uuid4())
    return new_uuid


class Auth:
    """ Auth class """
    def __init__(self):
        """ Constructor """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a user """
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """ Validates a login """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Creates a session """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """ Returns a User instance based on a session ID """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by_session_id(session_id)
            return user
        except NoResultFound:
            return None
