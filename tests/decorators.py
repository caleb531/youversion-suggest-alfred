#!/usr/bin/env python3
# coding=utf-8

import sys
from contextlib import contextmanager
from functools import wraps
from io import StringIO
from unittest.mock import patch


@contextmanager
def redirect_stdout():
    """Temporarily redirect stdout to a new text stream."""

    original_stdout = sys.stdout
    out = StringIO()
    try:
        sys.stdout = out
        yield out
    finally:
        sys.stdout = original_stdout


def use_user_prefs(user_prefs):
    """temporarily use the given values for user preferences"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with patch("yvs.core.get_user_prefs", return_value=user_prefs):
                return func(*args, **kwargs)

        return wrapper

    return decorator
