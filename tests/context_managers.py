#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contextlib import contextmanager
from io import BytesIO
import sys
import mock_modules
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
def preserve_prefs():
    """safely retrieve and restore preferences"""
    original_prefs = yvs.get_prefs()
    yield original_prefs.copy()
    yvs.update_prefs(original_prefs)


@contextmanager
def preserve_recent_refs():
    """safely retrieve and restore list of recent references"""
    original_recent_refs = yvs.get_recent_refs()
    yield original_recent_refs[:]
    yvs.update_recent_refs(original_recent_refs)


@contextmanager
def mock_webbrowser(yvs):
    mock = mock_modules.WebbrowserMock()
    original_webbrowser = yvs.webbrowser
    yvs.webbrowser = mock
    yield mock
    yvs.webbrowser = original_webbrowser
