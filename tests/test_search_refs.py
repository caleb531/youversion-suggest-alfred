#!/usr/bin/env python3
# coding=utf-8

import json
import re
from unittest.mock import Mock, NonCallableMock, patch

import yvs.core as core
import yvs.search_refs as search_refs
from tests.decorators import redirect_stdout, use_user_prefs

with open("tests/html/search.html") as html_file:
    patch_urlopen = patch(
        "urllib.request.urlopen",
        return_value=NonCallableMock(read=Mock(return_value=html_file.read())),
    )


def setup_function(function):
    patch_urlopen.start()


def teardown_function(function):
    patch_urlopen.stop()


def test_result_titles():
    """should correctly parse result titles from HTML"""

    results = search_refs.get_result_list("love others")

    assert re.search(r"^Romans 13:8 \(NIV\)", results[0]["title"])
    assert re.search(r"^John 15:12 \(NIV\)", results[1]["title"])
    assert re.search(r"^1 Peter 4:8 \(NIV\)", results[2]["title"])
    assert len(results) == 3


def test_result_subtitles():
    """should correctly parse result subtitles from HTML"""

    results = search_refs.get_result_list("love others")

    assert re.search("Lorem", results[0]["subtitle"])
    assert re.search("consectetur", results[1]["subtitle"])
    assert re.search("Ut aliquam", results[2]["subtitle"])
    assert len(results) == 3


def test_result_arg():
    """should correctly parse result UID arguments from HTML"""

    results = search_refs.get_result_list("love others")

    assert results[0]["arg"] == "111/rom.13.8"
    assert results[1]["arg"] == "111/jhn.15.12"
    assert results[2]["arg"] == "111/1pe.4.8"
    assert len(results) == 3


@patch("yvs.web.get_url_content", return_value="abc")
def test_unicode_input(get_url_content):
    """should correctly handle non-ASCII characters in query string"""

    search_refs.get_result_list("é")

    get_url_content.assert_called_with(
        "https://www.bible.com/search/bible?q=%C3%A9&version_id=111"
    )


def test_cache_url_content():
    """should cache search URL content after first fetch"""

    search_refs.get_result_list("love others")

    with patch("urllib.request.Request") as request:
        search_refs.get_result_list("love others")
        request.assert_not_called()


@use_user_prefs({"language": "eng", "version": 111, "copybydefault": False})
def test_copy_by_default_false():
    """should export correct data when "Copy By Default?" setting is false"""

    results = search_refs.get_result_list("love others")

    assert results[0]["variables"]["copybydefault"] == "False"
    assert results[0]["subtitle"] == "» “Lorem ipsum” dolor sit amet,"
    assert results[0]["mods"]["cmd"]["subtitle"] == "Copy content to clipboard"


@use_user_prefs({"language": "eng", "version": 111, "copybydefault": True})
def test_copy_by_default_true():
    """should export correct data when "Copy By Default?" setting is true"""

    results = search_refs.get_result_list("love others")

    assert results[0]["variables"]["copybydefault"] == "True"
    assert results[0]["subtitle"] == "» “Lorem ipsum” dolor sit amet,"
    assert results[0]["mods"]["cmd"]["subtitle"] == "View on YouVersion"


def test_structure():
    """JSON should match result list"""

    results = search_refs.get_result_list("love others")
    result = results[0]
    feedback_str = core.get_result_list_feedback_str(results)
    feedback = json.loads(feedback_str)

    assert "items" in feedback, "feedback object must have result items"
    item = feedback["items"][0]
    assert "uid" not in item
    assert item["arg"] == result["arg"]
    assert item["title"] == "Romans 13:8 (NIV) ♥"
    assert item["text"]["copy"] == result["title"]
    assert item["text"]["largetype"] == result["title"]
    assert item["subtitle"] == result["subtitle"]
    assert item["icon"]["path"] == "icon.png"


@patch("yvs.cache.get_cache_entry_content", return_value="<a>")
@patch("yvs.web.get_url_content", side_effect=search_refs.web.get_url_content)
def test_revalidate(get_cache_entry_content, get_url_content):
    """should re-fetch latest HTML when cached HTML can no longer be parsed"""

    query_str = "love others"
    results = search_refs.get_result_list(query_str)

    assert results != []
    assert get_url_content.call_count == 1


def test_output():
    """should output result list JSON"""

    query_str = "love others"

    with redirect_stdout() as out:
        search_refs.main(query_str)

    output = out.getvalue().rstrip()
    results = search_refs.get_result_list(query_str)
    feedback = core.get_result_list_feedback_str(results).rstrip()

    assert output == feedback


@patch("yvs.web.get_url_content", return_value="")
def test_null_result(get_url_content):
    """should output "No Results" JSON item for empty result list"""

    query_str = "xyz"

    with redirect_stdout() as out:
        search_refs.main(query_str)

    feedback = json.loads(out.getvalue())

    assert len(feedback["items"]) == 1, "result item is missing"
    item = feedback["items"][0]
    assert item["valid"] is False
    assert item["title"] == "No Results"


@patch("yvs.web.get_url_content", return_value="")
@patch(
    "yvs.search_refs.SearchResultParser.feed",
    side_effect=(Exception(), None),
)
def test_null_result_on_error(feed, get_url_content):
    """should output "No Results" JSON item even if parser errored"""

    query_str = "xyz"

    with redirect_stdout() as out:
        search_refs.main(query_str)

    feedback = json.loads(out.getvalue())

    assert len(feedback["items"]) == 1, "result item is missing"
    item = feedback["items"][0]
    assert item["valid"] is False
    assert item["title"] == "No Results"
