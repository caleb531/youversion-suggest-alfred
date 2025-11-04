#!/usr/bin/env python3
# coding=utf-8

import os
import os.path
import shutil

import yvs.clear_cache as clear_cache
from tests.decorators import redirect_stdout


def test_clear_cache():
    """should remove cache directory when cache is cleared"""

    with redirect_stdout():
        clear_cache.main()

    assert not os.path.exists(clear_cache.cache.LOCAL_CACHE_DIR_PATH), (
        "local cache directory exists"
    )


def test_clear_cache_silent_fail():
    """should fail silently if cache directory does not exist"""

    shutil.rmtree(clear_cache.cache.LOCAL_CACHE_DIR_PATH, ignore_errors=True)

    with redirect_stdout():
        clear_cache.main()

    assert not os.path.exists(clear_cache.cache.LOCAL_CACHE_DIR_PATH), (
        "local cache directory exists"
    )
