#!/usr/bin/env python3
# coding=utf-8

import json
import os
import os.path

import yvs.core as core
import yvs.set_pref as set_pref
from tests.decorators import redirect_stdout


def test_set_language():
    """should set preferred language"""

    set_pref.set_pref("language", "spa")
    user_prefs = core.get_user_prefs()

    assert user_prefs["language"] == "spa"
    bible = core.get_bible(user_prefs["language"])
    assert user_prefs["version"] == bible["default_version"]


def test_set_version():
    """should set preferred version"""

    set_pref.set_pref("version", 59)
    user_prefs = core.get_user_prefs()

    assert user_prefs["version"] == 59


def test_set_nonexistent():
    """should discard nonexistent preferences"""

    set_pref.set_pref("foo", "bar")
    user_prefs = core.get_user_prefs()

    assert "foo" not in user_prefs


def test_set_language_clear_cache():
    """should clear cache when setting language"""

    assert os.path.exists(set_pref.cache.LOCAL_CACHE_DIR_PATH), (
        "local cache directory does not exist"
    )

    set_pref.cache.add_cache_entry("foo", "blah blah")
    set_pref.set_pref("language", "spa")

    assert not os.path.exists(set_pref.cache.LOCAL_CACHE_DIR_PATH), (
        "local cache directory exists"
    )


def test_main():
    """should pass preference data to setter"""

    alfred_variables = {
        "pref_id": "version",
        "pref_name": "version",
        "value_id": "107",
        "value_name": "New English Translation",
    }

    with redirect_stdout() as out:
        set_pref.main(alfred_variables)

    alfred_json = json.loads(out.getvalue())
    assert alfred_json["alfredworkflow"]["variables"] == {"did_set_pref": "True"}

    user_prefs = core.get_user_prefs()
    assert user_prefs["version"] == 107
