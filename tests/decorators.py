# tests.decorators

import sys
import yvs.shared as yvs
from functools import wraps
from io import BytesIO


def redirect_stdout(fn):
    """temporarily redirect stdout to new output stream"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        original_stdout = sys.stdout
        out = BytesIO()
        try:
            sys.stdout = out
            return fn(out, *args, **kwargs)
        finally:
            sys.stdout = original_stdout
    return wrapper


def use_prefs(prefs):
    """temporarily use the given preferences"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            original_prefs = yvs.get_prefs()
            try:
                yvs.update_prefs(prefs)
                return fn(*args, **kwargs)
            finally:
                yvs.update_prefs(original_prefs)
        return wrapper
    return decorator
