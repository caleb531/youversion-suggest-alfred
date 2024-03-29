#!/usr/bin/env python3
# coding=utf-8

import os
import os.path
import shutil

import yvs.clear_cache as yvs
from tests import YVSTestCase


class TestClearCachw(YVSTestCase):

    def test_clear_cache(self):
        """should remove cache directory when cache is cleared"""
        yvs.main()
        self.assertFalse(
            os.path.exists(yvs.cache.LOCAL_CACHE_DIR_PATH),
            "local cache directory exists",
        )

    def test_clear_cache_silent_fail(self):
        """should fail silently if cache directory does not exist"""
        shutil.rmtree(yvs.cache.LOCAL_CACHE_DIR_PATH)
        yvs.main()
        self.assertFalse(
            os.path.exists(yvs.cache.LOCAL_CACHE_DIR_PATH),
            "local cache directory exists",
        )
