#!/usr/bin/env python3
# coding=utf-8

import glob
import json
import re

import yvs.core as core
import yvs.filter_prefs as filter_prefs
from tests.decorators import redirect_stdout, use_user_prefs


def test_show_languages():
    """should show all languages if no value is given"""

    results = filter_prefs.get_result_list("language")

    assert len(results) == len(glob.glob("yvs/data/bible/bible-*.json"))


def test_filter_languages():
    """should filter available languages if value is given"""

    results = filter_prefs.get_result_list("language esp")

    assert results[0]["uid"] == "yvs-language-spa"
    assert results[0]["title"] == "Español (América Latina)"
    assert results[0].get("valid", True) is True
    assert len(results) == 2
    assert results[0]["variables"] == {
        "pref_id": "language",
        "pref_name": "language",
        "value_id": '"spa"',
        "value_name": "Español (América Latina)",
    }


def test_filter_languages_non_latin():
    """should filter non-latin language names"""

    results = filter_prefs.get_result_list("language 繁")

    assert len(results) == 1
    assert results[0]["uid"] == "yvs-language-zho_tw"
    assert results[0]["title"] == "繁體中文"
    assert results[0].get("valid", True) is True
    assert results[0]["variables"] == {
        "pref_id": "language",
        "pref_name": "language",
        "value_id": '"zho_tw"',
        "value_name": "繁體中文",
    }


@use_user_prefs({"language": "spa", "version": 128, "refformat": "{name}\n{content}"})
def test_show_versions():
    """should show all versions if no value is given"""

    results = filter_prefs.get_result_list("version")

    assert len(results) > 10


def test_filter_versions():
    """should filter available versions if value is given"""

    results = filter_prefs.get_result_list("version ni")

    assert len(results) == 3
    assert results[0]["uid"] == "yvs-version-110"
    assert results[0]["title"] == "New International Reader’s Version (NIRV)"
    assert results[0].get("valid", True) is True
    assert results[0]["variables"] == {
        "pref_id": "version",
        "pref_name": "version",
        "value_id": "110",
        "value_name": "New International Reader’s Version (NIRV)",
    }


@use_user_prefs({"language": "spa", "version": 128, "refformat": "{name}\n{content}"})
def test_show_refformats():
    """should show all refformats if no value is given"""

    results = filter_prefs.get_result_list("refformat")

    assert len(results) > 3


def test_filter_refformats():
    """should filter available refformats if value is given"""

    results = filter_prefs.get_result_list("refformat http")
    result_title = '"Jesus wept." ¬ John 11:35 NIV ¬ {url}'.format(
        url=core.get_ref_url("111/jhn.11.35")
    )
    result_format_id = '"{content}"\n{name} {version}\n{url}'

    assert len(results) == 1
    assert results[0]["uid"] == f"yvs-refformat-{result_format_id}"
    assert results[0]["title"] == result_title
    assert results[0].get("valid", True) is True
    assert results[0]["variables"] == {
        "pref_id": "refformat",
        "pref_name": "reference format",
        "value_id": json.dumps(result_format_id),
        "value_name": result_title,
    }


@use_user_prefs({"language": "eng", "version": 59, "refformat": "Z {content}"})
def test_show_current_refformat():
    """should show current refformat as an available value"""

    results = filter_prefs.get_result_list("refformat Z")

    assert len(results) == 1
    assert results[0]["uid"] == "yvs-refformat-Z {content}"
    assert results[0]["title"] == "Z Jesus wept."
    assert results[0]["valid"] is False
    assert results[0]["variables"] == {
        "pref_id": "refformat",
        "pref_name": "reference format",
        "value_id": '"Z {content}"',
        "value_name": "Z Jesus wept.",
    }


def test_nonexistent_pref():
    """should not match nonexistent preference"""

    results = filter_prefs.get_result_list("xyz")

    assert len(results) == 0


def test_nonexistent_value():
    """should return null result for nonexistent value"""

    results = filter_prefs.get_result_list("language xyz")

    assert re.search("No Results", results[0]["title"])
    assert results[0]["valid"] is False
    assert len(results) == 1


def test_current_value():
    """should not make preference's current value actionable"""

    results = filter_prefs.get_result_list("language english")

    assert results[0]["title"] == "English"
    assert results[0]["valid"] is False
    assert len(results) == 1


def test_invalid_query():
    """should show all available preferences for invalid preference name"""

    results = filter_prefs.get_result_list("!@#")

    assert len(results) != 0


def test_show_all_preferences():
    """should show all available preferences if query is empty"""

    results = filter_prefs.get_result_list("")

    assert len(results) != 0


def test_preferences_autocompletion():
    """autocompletion should be functioning for all preference results"""

    results = filter_prefs.get_result_list("")

    for result in results:
        assert "autocomplete" in result
        assert "valid" in result
        assert result["valid"] is False


def test_filter_preferences_id():
    """should filter available preferences if partial pref ID is given"""

    results = filter_prefs.get_result_list("reff")

    assert len(results) == 1
    assert results[0]["uid"] == "yvs-refformat"
    assert results[0]["title"] == "Reference Format"


def test_filter_preferences_name():
    """should filter available preferences if partial pref name is given"""

    results = filter_prefs.get_result_list("refe")

    assert len(results) == 1
    assert results[0]["uid"] == "yvs-refformat"
    assert results[0]["title"] == "Reference Format"


def test_filter_preferences_name_partial():
    """should match partial pref name at word boundaries"""

    results = filter_prefs.get_result_list("version en sta v")

    assert len(results) == 1
    assert results[0]["uid"] == "yvs-version-59"
    assert results[0]["title"] == "English Standard Version 2016 (ESV)"


def test_filter_preferences_show_current():
    """should show current values for all preferences"""

    results = filter_prefs.get_result_list("")

    assert len(results) == 6
    assert "English" in results[0]["subtitle"]
    assert "NIV" in results[1]["subtitle"]


@use_user_prefs(
    {
        "language": "eng",
        "version": 999,
        "refformat": "{name}\n\n{content}",
        "versenumbers": False,
        "linebreaks": True,
        "copybydefault": True,
    }
)
def test_filter_preferences_show_current_valid_only():
    """should not show invalid current preference values"""

    results = filter_prefs.get_result_list("")

    assert len(results) == 6
    assert "currently" in results[0]["subtitle"]
    assert "currently" not in results[1]["subtitle"]


def test_filter_preference_entire_query():
    """should match available preference values using entire query string"""

    results = filter_prefs.get_result_list("language español (españa)")

    assert len(results) == 1
    assert results[0]["uid"] == "yvs-language-spa_es"
    assert results[0]["title"] == "Español (España)"
    assert results[0].get("valid", True) is True
    assert results[0]["variables"] == {
        "pref_id": "language",
        "pref_name": "language",
        "value_id": '"spa_es"',
        "value_name": "Español (España)",
    }


def test_filter_preference_ignore_special():
    """should ignore special characters when matching preference values"""

    results = filter_prefs.get_result_list("language 繁體中文$$")

    assert len(results) == 1
    assert results[0]["uid"] == "yvs-language-zho_tw"
    assert results[0]["title"] == "繁體中文"
    assert results[0].get("valid", True) is True
    assert results[0]["variables"] == {
        "pref_id": "language",
        "pref_name": "language",
        "value_id": '"zho_tw"',
        "value_name": "繁體中文",
    }


def test_main_output():
    """should output pref result list JSON"""

    query_str = "language"

    with redirect_stdout() as out:
        filter_prefs.main(query_str)

    output = out.getvalue().rstrip()
    results = filter_prefs.get_result_list(query_str)
    feedback = core.get_result_list_feedback_str(results).rstrip()

    assert output == feedback


def test_null_result():
    """should output "No Results" JSON item for empty pref result list"""

    query_str = "xyz"

    with redirect_stdout() as out:
        filter_prefs.main(query_str)

    feedback = json.loads(out.getvalue())

    assert len(feedback["items"]) == 1, "result item is missing"
    item = feedback["items"][0]
    assert item["title"] == "No Results"
    assert item["valid"] is False


def test_feedback_show_all():
    """should output JSON for all results if query is empty"""

    with redirect_stdout() as out:
        filter_prefs.main("")

    output = out.getvalue().rstrip()
    results = filter_prefs.get_result_list("")
    feedback = core.get_result_list_feedback_str(results).rstrip()

    assert output == feedback
