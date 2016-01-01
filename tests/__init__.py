# tests.__init__

import os
import os.path
import shutil
import tempfile
import yvs.shared as yvs
from mock import patch


temp_dir = tempfile.gettempdir()
yvs.LOCAL_DATA_DIR_PATH = os.path.join(temp_dir, 'yvs-data')
yvs.LOCAL_CACHE_DIR_PATH = os.path.join(temp_dir, 'yvs-cache')
yvs.USER_PREFS_PATH = os.path.join(yvs.LOCAL_DATA_DIR_PATH, 'preferences.json')


def mock_open(path, mode):
    if path.endswith('preferences.json'):
        path = yvs.USER_PREFS_PATH
    return open(path, mode)


patch_open = patch('yvs.shared.open', mock_open, create=True)


def set_up():
    try:
        os.mkdir(yvs.LOCAL_DATA_DIR_PATH)
    except OSError:
        pass
    try:
        os.mkdir(yvs.LOCAL_CACHE_DIR_PATH)
    except OSError:
        pass
    patch_open.start()


def tear_down():
    patch_open.stop()
    try:
        shutil.rmtree(yvs.LOCAL_CACHE_DIR_PATH)
    except OSError:
        pass
    try:
        shutil.rmtree(yvs.LOCAL_DATA_DIR_PATH)
    except OSError:
        pass
