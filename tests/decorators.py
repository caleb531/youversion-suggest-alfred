# tests.decorators

import sys
import yvs.shared as yvs
from functools import wraps
from io import BytesIO


def redirect_stdout(func):
    """temporarily redirect stdout to new output stream"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        original_stdout = sys.stdout
        out = BytesIO()
        try:
            sys.stdout = out
            return func(out, *args, **kwargs)
        finally:
            sys.stdout = original_stdout
    return wrapper


def use_user_prefs(user_prefs):
    """temporarily use the given values for user preferences"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            original_prefs = yvs.get_user_prefs()
            try:
                yvs.set_user_prefs(user_prefs)
                return func(*args, **kwargs)
            finally:
                yvs.set_user_prefs(original_prefs)
        return wrapper
    return decorator
