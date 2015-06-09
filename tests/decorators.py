#!/usr/bin/env python

from io import BytesIO
import sys
import yv_suggest.shared as yvs
from functools import wraps


def redirect_stdout(fn):
    """temporarily redirect stdout to new output stream"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        original_stdout = sys.stdout
        out = BytesIO()
        try:
            sys.stdout = out
            fn(out, *args, **kwargs)
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
                fn(*args, **kwargs)
            finally:
                yvs.update_prefs(original_prefs)
        return wrapper
    return decorator


def use_default_prefs(fn):
    """temporarily use the default values for all preferences"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        original_prefs = yvs.get_prefs()
        try:
            yvs.update_prefs(yvs.get_defaults())
            fn(*args, **kwargs)
        finally:
            yvs.update_prefs(original_prefs)
    return wrapper
