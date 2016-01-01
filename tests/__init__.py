# tests.__init__

import os
import os.path
import shutil
import tempfile
import yvs.shared as yvs
from mock import patch


yvs.LOCAL_DATA_DIR_PATH = os.path.join(tempfile.gettempdir(), 'yvs')
yvs.USER_PREFS_PATH = os.path.join(yvs.LOCAL_DATA_DIR_PATH, 'preferences.json')


def mock_open(path, mode):
    if path.endswith('preferences.json'):
        path = yvs.USER_PREFS_PATH
    return open(path, mode)


patch_open = patch('yvs.shared.open', mock_open, create=True)


def setup():
    try:
        os.mkdir(yvs.LOCAL_DATA_DIR_PATH)
    except OSError:
        pass
    patch_open.start()


def teardown():
    patch_open.stop()
    shutil.rmtree(yvs.LOCAL_DATA_DIR_PATH)
