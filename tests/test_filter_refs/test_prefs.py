#!/usr/bin/env python3
# coding=utf-8

import os.path

import pytest

import yvs.core as core
import yvs.filter_refs as filter_refs
from tests.decorators import use_user_prefs


@use_user_prefs({"language": "eng", "version": 59, "copybydefault": False})
def test_version_persistence():
    """should remember version preferences"""

    results = filter_refs.get_result_list("mat 4")

    assert results[0]["title"] == "Matthew 4 (ESV)"
    assert len(results) == 1


@use_user_prefs({"language": "spa", "version": 128, "copybydefault": False})
def test_language_persistence():
    """should remember language preferences"""

    results = filter_refs.get_result_list("gá 4")

    assert results[0]["title"] == "Gálatas 4 (NVI)"
    assert len(results) == 1


def test_missing_prefs():
    """should supply missing preferences with defaults"""

    core.set_user_prefs({})
    results = filter_refs.get_result_list("mat 5.3")

    assert len(results) == 1


@use_user_prefs({"language": "eng", "version": 999, "copybydefault": False})
def test_invalid_user_version():
    """should raise exception when invalid version is set"""

    with pytest.raises(Exception):
        filter_refs.get_result_list("ph 4")


@use_user_prefs({"language": "eng", "version": 111, "copybydefault": False})
def test_copy_by_default_false():
    """should export correct data when "Copy By Default?" setting is false"""

    results = filter_refs.get_result_list("mat 5.3")

    assert results[0]["variables"]["copybydefault"] == "False"
    assert results[0]["subtitle"] == "View on YouVersion"
    assert results[0]["mods"]["cmd"]["subtitle"] == "Copy content to clipboard"


@use_user_prefs({"language": "eng", "version": 111, "copybydefault": True})
def test_copy_by_default_true():
    """should export correct data when "Copy By Default?" setting is true"""

    results = filter_refs.get_result_list("mat 5.3")

    assert results[0]["variables"]["copybydefault"] == "True"
    assert results[0]["subtitle"] == "Copy content to clipboard"
    assert results[0]["mods"]["cmd"]["subtitle"] == "View on YouVersion"


def test_create_local_data_dir_silent_fail():
    """should silently fail if local data directory already exists"""

    core.create_local_data_dir()
    core.create_local_data_dir()

    assert os.path.exists(core.LOCAL_DATA_DIR_PATH), (
        "local data directory does not exist"
    )


def test_prettified_prefs_json():
    core.set_user_prefs(
        {"language": "spa", "version": 128, "refformat": "{name}\n{content}"}
    )

    with open(core.get_user_prefs_path(), "r") as user_prefs_file:
        user_prefs_json = user_prefs_file.read()

    assert "\n  " in user_prefs_json, "User prefs JSON is not prettified"
