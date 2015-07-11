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


def use_prefs(prefs):
    """temporarily use the given preferences"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            original_prefs = yvs.get_prefs()
            try:
                yvs.update_prefs(prefs)
                return func(*args, **kwargs)
            finally:
                yvs.update_prefs(original_prefs)
        return wrapper
    return decorator
