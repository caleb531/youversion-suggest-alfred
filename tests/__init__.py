# tests.__init__

import os
import os.path
import shutil
import tempfile
import yvs.shared as yvs
from mock import patch


yvs.ALFRED_DATA_DIR = os.path.join(tempfile.gettempdir(), 'yvs')
yvs.PREFS_PATH = os.path.join(yvs.ALFRED_DATA_DIR, 'preferences.json')
os.mkdir(yvs.ALFRED_DATA_DIR)


def mock_open(path, mode):
    if path.endswith('preferences.json'):
        path = yvs.PREFS_PATH
    return open(path, mode)


patch_open = patch('yvs.shared.open', mock_open, create=True)


def setup():
    patch_open.start()


def teardown():
    patch_open.stop()
    shutil.rmtree(yvs.ALFRED_DATA_DIR)
