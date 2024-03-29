#!/usr/bin/env python3
# coding=utf-8

import json

import yvs.filter_refs as yvs
from tests import YVSTestCase


class TestFeedback(YVSTestCase):

    def test_validity(self):
        """should return syntactically-valid JSON"""
        results = yvs.get_result_list("john 3:16")
        feedback_str = yvs.core.get_result_list_feedback_str(results)
        self.assertIsInstance(json.loads(feedback_str), dict)

    def test_structure(self):
        """JSON should match result list"""
        results = yvs.get_result_list("matthew 6:34")
        result = results[0]
        feedback_str = yvs.core.get_result_list_feedback_str(results)
        feedback = json.loads(feedback_str)
        self.assertIn("items", feedback, "feedback object must have result items")
        item = feedback["items"][0]
        self.assertEqual(item["uid"], result["uid"])
        self.assertEqual(item["arg"], result["arg"])
        self.assertEqual(item["title"], "Matthew 6:34 (NIV)")
        self.assertEqual(item["text"]["copy"], result["title"])
        self.assertEqual(item["text"]["largetype"], result["title"])
        self.assertEqual(item["subtitle"], result["subtitle"])
        self.assertEqual(item["icon"]["path"], "icon.png")
