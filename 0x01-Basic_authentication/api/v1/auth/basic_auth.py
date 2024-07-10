#!/usr/bin/env python3
""" Module of BasicAuth views"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple


class BasicAuth(Auth):
    """BasicAuth class.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header value.

        Returns:
            str: The Base64 part of the Authorization header,or None if
            invalid.
        """
        if authorization_header is None or not isinstance(authorization_header,
                                                          str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ", 1)[1]

    def decode_base64_authorization_header(
                        self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 value of an Authorization header.

        Args:
            base64_authorization_header (str): The Base64-encoded
                            Authorization header.

        Returns:
            str: The decoded value as a UTF-8 string, or None if invalid.
        """
        try:
            if base64_authorization_header is None or not isinstance(
                                        base64_authorization_header, str):
                return None
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extracts the user email and password from the Base64-decoded
        Authorization header.

        Args:
            decoded_base64_authorization_header (str): The Base64-decoded
            Authorization header.

        Returns:
            Tuple[str, str]: The user email and password, or
            (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None or not isinstance(
                                    decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password
