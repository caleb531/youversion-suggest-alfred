# tests.test_add_language.__init__

import os
import os.path
import shutil
import tempfile

from mock import patch

import tests
import yvs.shared as yvs

temp_dir = tempfile.gettempdir()
packaged_data_dir_path_patcher = patch(
    'yvs.shared.PACKAGED_DATA_DIR_PATH',
    os.path.join(temp_dir, 'yvs-core'))


def set_up():
    orig_packaged_data_dir_path = yvs.PACKAGED_DATA_DIR_PATH
    packaged_data_dir_path_patcher.start()
    try:
        shutil.copytree(
            orig_packaged_data_dir_path, yvs.PACKAGED_DATA_DIR_PATH)
    except shutil.Error:
        pass
    tests.set_up()


def tear_down():
    try:
        shutil.rmtree(yvs.PACKAGED_DATA_DIR_PATH)
    except OSError:
        pass
    packaged_data_dir_path_patcher.stop()
    tests.tear_down()
