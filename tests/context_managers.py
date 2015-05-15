#!/usr/bin/env python

from contextlib import contextmanager
from io import BytesIO
import sys
import module_mocks
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
def use_prefs(prefs):
    """temporarily use the given preferences"""
    original_prefs = yvs.get_prefs()
    try:
        yvs.update_prefs(prefs)
        yield
    finally:
        yvs.update_prefs(original_prefs)


@contextmanager
def use_default_prefs():
    """temporarily use the default values for all preferences"""
    original_prefs = yvs.get_prefs()
    try:
        yvs.update_prefs(yvs.get_defaults())
        yield
    finally:
        yvs.update_prefs(original_prefs)


@contextmanager
def mock_webbrowser(yvs):
    """mock the webbrowser module for testing purposes"""
    mock = module_mocks.WebbrowserMock()
    original_webbrowser = yvs.webbrowser
    yvs.webbrowser = mock
    try:
        yield mock
    finally:
        yvs.webbrowser = original_webbrowser
