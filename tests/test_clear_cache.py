#!/usr/bin/env python3
# coding=utf-8

import os
import os.path
import shutil
import unittest

from nose2.tools.decorators import with_setup, with_teardown

import yvs.clear_cache as yvs
from tests import set_up, tear_down


case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
def test_clear_cache():
    """should remove cache directory when cache is cleared"""
    yvs.main()
    case.assertFalse(
        os.path.exists(yvs.cache.LOCAL_CACHE_DIR_PATH),
        'local cache directory exists')


@with_setup(set_up)
@with_teardown(tear_down)
def test_clear_cache_silent_fail():
    """should fail silently if cache directory does not exist"""
    shutil.rmtree(yvs.cache.LOCAL_CACHE_DIR_PATH)
    yvs.main()
    case.assertFalse(
        os.path.exists(yvs.cache.LOCAL_CACHE_DIR_PATH),
        'local cache directory exists')
