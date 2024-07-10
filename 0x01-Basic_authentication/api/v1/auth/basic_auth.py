#!/usr/bin/env python3
""" Module of BasicAuth views"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
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
