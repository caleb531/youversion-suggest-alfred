#!/usr/bin/env python3
# coding=utf-8

import os
import os.path
import shutil

import yvs.clear_cache as clear_cache
from tests import YVSTestCase
from tests.decorators import redirect_stdout


class TestClearCachw(YVSTestCase):
    @redirect_stdout
    def test_clear_cache(self, out):
        """should remove cache directory when cache is cleared"""
        clear_cache.main()
        self.assertFalse(
            os.path.exists(clear_cache.cache.LOCAL_CACHE_DIR_PATH),
            "local cache directory exists",
        )

    @redirect_stdout
    def test_clear_cache_silent_fail(self, out):
        """should fail silently if cache directory does not exist"""
        shutil.rmtree(clear_cache.cache.LOCAL_CACHE_DIR_PATH)
        clear_cache.main()
        self.assertFalse(
            os.path.exists(clear_cache.cache.LOCAL_CACHE_DIR_PATH),
            "local cache directory exists",
        )
