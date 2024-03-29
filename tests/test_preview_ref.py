#!/usr/bin/env python3
# coding=utf-8

import json
from unittest.mock import Mock, NonCallableMock, patch

import yvs.preview_ref as yvs
from tests import YVSTestCase
from tests.decorators import redirect_stdout, use_user_prefs

with open("tests/html/psa.23.html") as html_file:
    patch_urlopen = patch(
        "urllib.request.urlopen",
        return_value=NonCallableMock(read=Mock(return_value=html_file.read())),
    )


class TestPreviewRef(YVSTestCase):

    def setUp(self):
        patch_urlopen.start()
        super().setUp()

    def tearDown(self):
        patch_urlopen.stop()
        super().tearDown()

    @redirect_stdout
    def test_preview_chapter(self, out):
        """should preview reference content for chapter"""
        yvs.main("111/psa.23")
        preview_feedback = json.loads(out.getvalue())
        self.assertNotRegex(preview_feedback["response"], "David")
        self.assertRegex(preview_feedback["response"], "Lorem")
        self.assertRegex(preview_feedback["response"], "nunc nulla")
        self.assertRegex(preview_feedback["response"], "fermentum")
        self.assertIn("Psalms 23 (NIV)", preview_feedback["footer"])

    @redirect_stdout
    def test_preview_verse(self, out):
        """should preview reference content for verse"""
        yvs.main("59/psa.23.2")
        preview_feedback = json.loads(out.getvalue())
        self.assertNotRegex(preview_feedback["response"], "Lorem")
        self.assertRegex(preview_feedback["response"], "nunc nulla")
        self.assertNotRegex(preview_feedback["response"], "fermentum")
        self.assertIn("Psalms 23:2 (ESV)", preview_feedback["footer"])

    @use_user_prefs(
        {
            "language": "eng",
            "version": 59,
            "refformat": "{name} ({version})\n\n{content}",
            "versenumbers": False,
            "linebreaks": True,
            "copybydefault": True,
        }
    )
    @redirect_stdout
    def test_copybydefault_yes(self, out):
        """should display copy action when copybydefault is enabled"""
        yvs.main("59/psa.23.2")
        preview_feedback = json.loads(out.getvalue())
        self.assertIn("Copy content to clipboard", preview_feedback["footer"])
        self.assertNotIn("View on YouVersion", preview_feedback["footer"])

    @use_user_prefs(
        {
            "language": "eng",
            "version": 59,
            "refformat": "{name} ({version})\n\n{content}",
            "versenumbers": False,
            "linebreaks": True,
            "copybydefault": False,
        }
    )
    @redirect_stdout
    def test_copybydefault_no(self, out):
        """should display view action when copybydefault is disabled"""
        yvs.main("59/psa.23.2")
        preview_feedback = json.loads(out.getvalue())
        self.assertIn("View on YouVersion", preview_feedback["footer"])
        self.assertNotIn("Copy content to clipboard", preview_feedback["footer"])

    @use_user_prefs(
        {
            "language": "eng",
            "version": 59,
            "refformat": '{name}\n"{content}"',
            "versenumbers": False,
            "linebreaks": True,
            "copybydefault": False,
        }
    )
    @redirect_stdout
    def test_refformat(self, out):
        """
        should bypass user's refformat and use consistent refformat for preview
        """
        yvs.main("59/psa.23.2")
        preview_feedback = json.loads(out.getvalue())
        self.assertIn("Psalms 23:2 (ESV)\n\n", preview_feedback["response"])
        self.assertNotIn("- Psalms 23:2\n", preview_feedback["response"])
