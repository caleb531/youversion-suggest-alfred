#!/usr/bin/env python3
# coding=utf-8


import yvs.filter_refs as filter_refs
from tests import YVSTestCase
from tests.decorators import use_user_prefs


class TestShorthand(YVSTestCase):

    def test_book(self):
        """should recognize shorthand book syntax"""
        results = filter_refs.get_result_list("1co")
        self.assertEqual(results[0]["title"], "1 Corinthians 1 (NIV)")
        self.assertEqual(len(results), 1)

    def test_chapter(self):
        """should recognize shorthand chapter syntax"""
        results = filter_refs.get_result_list("1 co13")
        self.assertEqual(results[0]["title"], "1 Corinthians 13 (NIV)")
        self.assertEqual(len(results), 1)

    def test_version(self):
        """should recognize shorthand version syntax"""
        results = filter_refs.get_result_list("1 co 13esv")
        self.assertEqual(results[0]["title"], "1 Corinthians 13 (ESV)")
        self.assertEqual(len(results), 1)

    @use_user_prefs({"language": "zho_tw", "version": 46, "copybydefault": False})
    def test_version_unicode(self):
        """should allow shorthand Unicode versions"""
        results = filter_refs.get_result_list("創世記1:3次經")
        self.assertEqual(results[0]["title"], "創世記 1:3 (次經)")
        self.assertEqual(len(results), 1)
