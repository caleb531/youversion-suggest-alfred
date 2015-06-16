#!/usr/bin/env python

import os
import tempfile
from mock import patch


PREFS_PATH = os.path.join(tempfile.gettempdir(), 'yvs-preferences.json')


def mock_open(path, mode):
    if path.endswith('preferences.json'):
        path = PREFS_PATH
    return open(path, mode)


def setup():
    global patch_open
    patch_open = patch('yv_suggest.shared.open', mock_open, create=True)
    patch_open.start()


def teardown():
    patch_open.stop()
    os.remove(PREFS_PATH)
