# tests.__init__

import os
import os.path
import shutil
import tempfile

import yvs.shared as yvs
from mock import patch


temp_dir = tempfile.gettempdir()
local_data_dir_patcher = patch(
    'yvs.shared.LOCAL_DATA_DIR_PATH',
    os.path.join(temp_dir, 'yvs-data'))
local_cache_dir_patcher = patch(
    'yvs.shared.LOCAL_CACHE_DIR_PATH',
    os.path.join(temp_dir, 'yvs-cache'))


def set_up():
    local_data_dir_patcher.start()
    try:
        os.mkdir(yvs.LOCAL_DATA_DIR_PATH)
    except OSError:
        pass
    local_cache_dir_patcher.start()
    try:
        os.mkdir(yvs.LOCAL_CACHE_DIR_PATH)
    except OSError:
        pass


def tear_down():
    try:
        shutil.rmtree(yvs.LOCAL_CACHE_DIR_PATH)
    except OSError:
        pass
    local_cache_dir_patcher.stop()
    try:
        shutil.rmtree(yvs.LOCAL_DATA_DIR_PATH)
    except OSError:
        pass
    local_data_dir_patcher.stop()
