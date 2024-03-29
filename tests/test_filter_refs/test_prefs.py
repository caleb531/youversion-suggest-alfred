#!/usr/bin/env python3
# coding=utf-8

import os.path

import yvs.filter_refs as yvs
from tests import YVSTestCase
from tests.decorators import use_user_prefs


class TestPrefs(YVSTestCase):

    @use_user_prefs({"language": "eng", "version": 59, "copybydefault": False})
    def test_version_persistence(self):
        """should remember version preferences"""
        results = yvs.get_result_list("mat 4")
        self.assertEqual(results[0]["title"], "Matthew 4 (ESV)")
        self.assertEqual(len(results), 1)

    @use_user_prefs({"language": "spa", "version": 128, "copybydefault": False})
    def test_language_persistence(self):
        """should remember language preferences"""
        results = yvs.get_result_list("gá 4")
        self.assertEqual(results[0]["title"], "Gálatas 4 (NVI)")
        self.assertEqual(len(results), 1)

    def test_missing_prefs(self):
        """should supply missing preferences with defaults"""
        yvs.core.set_user_prefs({})
        results = yvs.get_result_list("mat 5.3")
        self.assertEqual(len(results), 1)

    @use_user_prefs({"language": "eng", "version": 999, "copybydefault": False})
    def test_invalid_user_version(self):
        """should raise exception when invalid version is set"""
        with self.assertRaises(Exception):
            yvs.get_result_list("ph 4")

    @use_user_prefs({"language": "eng", "version": 111, "copybydefault": False})
    def test_copy_by_default_false(self):
        """should export correct data when "Copy By Default?" setting is false"""
        results = yvs.get_result_list("mat 5.3")
        self.assertEqual(results[0]["variables"]["copybydefault"], "False")
        self.assertEqual(results[0]["subtitle"], "View on YouVersion")
        self.assertEqual(
            results[0]["mods"]["cmd"]["subtitle"], "Copy content to clipboard"
        )

    @use_user_prefs({"language": "eng", "version": 111, "copybydefault": True})
    def test_copy_by_default_true(self):
        """should export correct data when "Copy By Default?" setting is true"""
        results = yvs.get_result_list("mat 5.3")
        self.assertEqual(results[0]["variables"]["copybydefault"], "True")
        self.assertEqual(results[0]["subtitle"], "Copy content to clipboard")
        self.assertEqual(results[0]["mods"]["cmd"]["subtitle"], "View on YouVersion")

    def test_create_local_data_dir_silent_fail(self):
        """should silently fail if local data directory already exists"""
        yvs.core.create_local_data_dir()
        yvs.core.create_local_data_dir()
        self.assertTrue(
            os.path.exists(yvs.core.LOCAL_DATA_DIR_PATH),
            "local data directory does not exist",
        )

    def test_prettified_prefs_json(self):
        yvs.core.set_user_prefs(
            {"language": "spa", "version": 128, "refformat": "{name}\n{content}"}
        )
        with open(yvs.core.get_user_prefs_path(), "r") as user_prefs_file:
            user_prefs_json = user_prefs_file.read()
            self.assertIn("\n  ", user_prefs_json, "User prefs JSON is not prettified")
