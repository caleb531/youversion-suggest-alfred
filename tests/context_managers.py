#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contextlib import contextmanager
from io import BytesIO
import sys


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
