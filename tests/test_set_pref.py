#!/usr/bin/env python3
# coding=utf-8

import json
import os
import os.path

import yvs.set_pref as yvs
from tests import YVSTestCase
from tests.decorators import redirect_stdout


class TestSetPref(YVSTestCase):

    def test_set_language(self):
        """should set preferred language"""
        yvs.set_pref("language", "spa")
        user_prefs = yvs.core.get_user_prefs()
        self.assertEqual(user_prefs["language"], "spa")
        bible = yvs.core.get_bible(user_prefs["language"])
        self.assertEqual(user_prefs["version"], bible["default_version"])

    def test_set_version(self):
        """should set preferred version"""
        yvs.set_pref("version", 59)
        user_prefs = yvs.core.get_user_prefs()
        self.assertEqual(user_prefs["version"], 59)

    def test_set_nonexistent(self):
        """should discard nonexistent preferences"""
        yvs.set_pref("foo", "bar")
        user_prefs = yvs.core.get_user_prefs()
        self.assertNotIn("foo", user_prefs)

    def test_set_language_clear_cache(self):
        """should clear cache when setting language"""
        self.assertTrue(
            os.path.exists(yvs.cache.LOCAL_CACHE_DIR_PATH),
            "local cache directory does not exist",
        )
        yvs.cache.add_cache_entry("foo", "blah blah")
        yvs.set_pref("language", "spa")
        self.assertFalse(
            os.path.exists(yvs.cache.LOCAL_CACHE_DIR_PATH),
            "local cache directory exists",
        )

    @redirect_stdout
    def test_main(self, out):
        """should pass preference data to setter"""
        alfred_variables = {
            "pref_id": "version",
            "pref_name": "version",
            "value_id": "107",
            "value_name": "New English Translation",
        }
        yvs.main(alfred_variables)
        alfred_json = json.loads(out.getvalue())
        self.assertEqual(alfred_json["alfredworkflow"]["variables"], alfred_variables)
        user_prefs = yvs.core.get_user_prefs()
        self.assertEqual(user_prefs["version"], 107)
