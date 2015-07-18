# tests.__init__

import os
import tempfile
from mock import patch


PREFS_PATH = os.path.join(tempfile.gettempdir(), 'yvs-preferences.json')


def mock_open(path, mode):
    if path.endswith('preferences.json'):
        path = PREFS_PATH
    return open(path, mode)


patch_open = patch('yvs.shared.open', mock_open, create=True)


def setup():
    patch_open.start()


def teardown():
    patch_open.stop()
    os.remove(PREFS_PATH)
