#!/usr/bin/env python3
# coding=utf-8

import shutil
from unittest.mock import patch

import pytest

import yvs.cache as cache
import yvs.core as core


@pytest.fixture(autouse=True)
def patch_local_dirs(tmp_path_factory):
    """Ensure tests use isolated cache and data directories."""
    data_path = str(tmp_path_factory.mktemp("yvs-data"))
    cache_path = str(tmp_path_factory.mktemp("yvs-cache"))

    try:
        with (
            patch.object(core, "LOCAL_DATA_DIR_PATH", data_path),
            patch.object(cache, "LOCAL_CACHE_DIR_PATH", cache_path),
        ):
            yield
    finally:
        shutil.rmtree(cache_path, ignore_errors=True)
        shutil.rmtree(data_path, ignore_errors=True)
