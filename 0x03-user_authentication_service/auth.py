#!/usr/bin/env python3
"""auth.py module"""

import bcrypt
import logging


logging.disable(logging.WARNING)


def _hash_password(password: str) -> bytes:
    """Hashes a user's input password"""

    hashed_p = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hashed_p
