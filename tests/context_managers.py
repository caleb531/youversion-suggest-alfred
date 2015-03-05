#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contextlib import contextmanager
from io import BytesIO
import sys
import yv_suggest.shared as yvs


@contextmanager
def redirect_stdout():
    """temporarily redirect stdout to new output stream"""
    original_stdout = sys.stdout
    out = BytesIO()
    try:
        sys.stdout = out
        yield out
    finally:
        sys.stdout = original_stdout


@contextmanager
def get_prefs():
    """safely retrieve and restore preferences"""
    original_prefs = yvs.get_prefs()
    yield original_prefs.copy()
    yvs.update_prefs(original_prefs)
