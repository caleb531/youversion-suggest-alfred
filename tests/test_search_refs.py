#!/usr/bin/env python3
# coding=utf-8

import json
from unittest.mock import Mock, NonCallableMock, patch

import yvs.core as core
import yvs.search_refs as search_refs
from tests import YVSTestCase
from tests.decorators import redirect_stdout, use_user_prefs

with open("tests/html/search.html") as html_file:
    patch_urlopen = patch(
        "urllib.request.urlopen",
        return_value=NonCallableMock(read=Mock(return_value=html_file.read())),
    )


class TestSearchRefs(YVSTestCase):

    def setUp(self):
        patch_urlopen.start()
        super().setUp()

    def tearDown(self):
        patch_urlopen.stop()
        super().tearDown()

    def test_result_titles(self):
        """should correctly parse result titles from HTML"""
        results = search_refs.get_result_list("love others")
        self.assertRegex(results[0]["title"], r"^Romans 13:8 \(NIV\)")
        self.assertRegex(results[1]["title"], r"^John 15:12 \(NIV\)")
        self.assertRegex(results[2]["title"], r"^1 Peter 4:8 \(NIV\)")
        self.assertEqual(len(results), 3)

    def test_result_subtitles(self):
        """should correctly parse result subtitles from HTML"""
        results = search_refs.get_result_list("love others")
        self.assertRegex(results[0]["subtitle"], "Lorem")
        self.assertRegex(results[1]["subtitle"], "consectetur")
        self.assertRegex(results[2]["subtitle"], "Ut aliquam")
        self.assertEqual(len(results), 3)

    def test_result_arg(self):
        """should correctly parse result UID arguments from HTML"""
        results = search_refs.get_result_list("love others")
        self.assertEqual(results[0]["arg"], "111/rom.13.8")
        self.assertEqual(results[1]["arg"], "111/jhn.15.12")
        self.assertEqual(results[2]["arg"], "111/1pe.4.8")
        self.assertEqual(len(results), 3)

    @patch("yvs.web.get_url_content", return_value="abc")
    def test_unicode_input(self, get_url_content):
        """should correctly handle non-ASCII characters in query string"""
        search_refs.get_result_list("é")
        get_url_content.assert_called_with(
            "https://www.bible.com/search/bible?q=%C3%A9&version_id=111"
        )

    def test_cache_url_content(self):
        """should cache search URL content after first fetch"""
        search_refs.get_result_list("love others")
        with patch("urllib.request.Request") as request:
            search_refs.get_result_list("love others")
            request.assert_not_called()

    @use_user_prefs({"language": "eng", "version": 111, "copybydefault": False})
    def test_copy_by_default_false(self):
        """should export correct data when "Copy By Default?" setting is false"""
        results = search_refs.get_result_list("love others")
        self.assertEqual(results[0]["variables"]["copybydefault"], "False")
        self.assertEqual(results[0]["subtitle"], "» “Lorem ipsum” dolor sit amet,")
        self.assertEqual(
            results[0]["mods"]["cmd"]["subtitle"], "Copy content to clipboard"
        )

    @use_user_prefs({"language": "eng", "version": 111, "copybydefault": True})
    def test_copy_by_default_true(self):
        """should export correct data when "Copy By Default?" setting is true"""
        results = search_refs.get_result_list("love others")
        self.assertEqual(results[0]["variables"]["copybydefault"], "True")
        self.assertEqual(results[0]["subtitle"], "» “Lorem ipsum” dolor sit amet,")
        self.assertEqual(results[0]["mods"]["cmd"]["subtitle"], "View on YouVersion")

    def test_structure(self):
        """JSON should match result list"""
        results = search_refs.get_result_list("love others")
        result = results[0]
        feedback_str = core.get_result_list_feedback_str(results)
        feedback = json.loads(feedback_str)
        self.assertIn("items", feedback, "feedback object must have result items")
        item = feedback["items"][0]
        self.assertNotIn("uid", item)
        self.assertEqual(item["arg"], result["arg"])
        self.assertEqual(item["title"], "Romans 13:8 (NIV) ♥")
        self.assertEqual(item["text"]["copy"], result["title"])
        self.assertEqual(item["text"]["largetype"], result["title"])
        self.assertEqual(item["subtitle"], result["subtitle"])
        self.assertEqual(item["icon"]["path"], "icon.png")

    @patch("yvs.cache.get_cache_entry_content", return_value="<a>")
    @patch("yvs.web.get_url_content", side_effect=search_refs.web.get_url_content)
    def test_revalidate(self, get_cache_entry_content, get_url_content):
        """should re-fetch latest HTML when cached HTML can no longer be parsed"""
        query_str = "love others"
        results = search_refs.get_result_list(query_str)
        self.assertNotEqual(results, [])
        self.assertEqual(get_url_content.call_count, 1)

    @redirect_stdout
    def test_output(self, out):
        """should output result list JSON"""
        query_str = "love others"
        search_refs.main(query_str)
        output = out.getvalue().rstrip()
        results = search_refs.get_result_list(query_str)
        feedback = core.get_result_list_feedback_str(results).rstrip()
        self.assertEqual(output, feedback)

    @redirect_stdout
    @patch("yvs.web.get_url_content", return_value="")
    def test_null_result(self, out, get_url_content):
        """should output "No Results" JSON item for empty result list"""
        query_str = "xyz"
        search_refs.main(query_str)
        feedback_str = out.getvalue()
        feedback = json.loads(feedback_str)
        self.assertEqual(len(feedback["items"]), 1, "result item is missing")
        item = feedback["items"][0]
        self.assertEqual(item["valid"], False)
        self.assertEqual(item["title"], "No Results")

    @redirect_stdout
    @patch("yvs.web.get_url_content", return_value="")
    @patch("yvs.search_refs.SearchResultParser.feed", side_effect=(Exception(), None))
    def test_null_result_on_error(self, out, feed, get_url_content):
        """should output "No Results" JSON item even if parser errored"""
        query_str = "xyz"
        search_refs.main(query_str)
        feedback_str = out.getvalue()
        feedback = json.loads(feedback_str)
        self.assertEqual(len(feedback["items"]), 1, "result item is missing")
        item = feedback["items"][0]
        self.assertEqual(item["valid"], False)
        self.assertEqual(item["title"], "No Results")
