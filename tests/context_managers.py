#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    """safely retrieve and restore preferences"""
    original_prefs = yvs.get_prefs()
    try:
        if prefs == {}:
            prefs = yvs.get_defaults()
        yvs.update_prefs(prefs)
        yield
    finally:
        yvs.update_prefs(original_prefs)


@contextmanager
def use_recent_refs(recent_refs):
    """safely retrieve and restore list of recent references"""
    original_recent_refs = yvs.get_recent_refs()
    try:
        yvs.update_recent_refs(recent_refs)
        yield
    finally:
        yvs.update_recent_refs(original_recent_refs)


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
