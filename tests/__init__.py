# tests.__init__

import os
import os.path
import shutil
import tempfile
import yvs.shared as yvs


temp_dir = tempfile.gettempdir()
yvs.LOCAL_DATA_DIR_PATH = os.path.join(temp_dir, 'yvs-data')
yvs.LOCAL_CACHE_DIR_PATH = os.path.join(temp_dir, 'yvs-cache')


def set_up():
    try:
        os.mkdir(yvs.LOCAL_DATA_DIR_PATH)
    except OSError:
        pass
    try:
        os.mkdir(yvs.LOCAL_CACHE_DIR_PATH)
    except OSError:
        pass


def tear_down():
    try:
        shutil.rmtree(yvs.LOCAL_CACHE_DIR_PATH)
    except OSError:
        pass
    try:
        shutil.rmtree(yvs.LOCAL_DATA_DIR_PATH)
    except OSError:
        pass
