#!/usr/bin/env python3
# coding=utf-8

import os
import os.path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import yvs.cache as cache
import yvs.core as core

temp_dir = tempfile.gettempdir()
local_data_dir_patcher = patch(
    "yvs.core.LOCAL_DATA_DIR_PATH", os.path.join(temp_dir, "yvs-data")
)
local_cache_dir_patcher = patch(
    "yvs.cache.LOCAL_CACHE_DIR_PATH", os.path.join(temp_dir, "yvs-cache")
)


class YVSTestCase(unittest.TestCase):

    def setUp(self):
        local_data_dir_patcher.start()
        try:
            os.makedirs(core.LOCAL_DATA_DIR_PATH)
        except OSError:
            pass
        local_cache_dir_patcher.start()
        try:
            os.makedirs(cache.LOCAL_CACHE_DIR_PATH)
        except OSError:
            pass

    def tearDown(self):
        try:
            shutil.rmtree(cache.LOCAL_CACHE_DIR_PATH)
        except OSError:
            pass
        local_cache_dir_patcher.stop()
        try:
            shutil.rmtree(core.LOCAL_DATA_DIR_PATH)
        except OSError:
            pass
        local_data_dir_patcher.stop()
