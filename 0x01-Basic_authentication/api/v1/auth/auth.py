#!/usr/bin/env python3
""" Module of Index views"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Auth class.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of excluded paths.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if path == excluded_path or excluded_path.startswith(path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Placeholder method for retrieving authorization header.
        Returns None for now.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder method for getting the current user.
        Returns None for now.
        """
        return None
