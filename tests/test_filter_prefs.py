#!/usr/bin/env python3
# coding=utf-8

import glob
import json

import yvs.core as core
import yvs.filter_prefs as filter_prefs
from tests import YVSTestCase
from tests.decorators import redirect_stdout, use_user_prefs


class TestFilterPrefs(YVSTestCase):
    def test_show_languages(self):
        """should show all languages if no value is given"""
        results = filter_prefs.get_result_list("language")
        self.assertEqual(len(results), len(glob.glob("yvs/data/bible/bible-*.json")))

    def test_filter_languages(self):
        """should filter available languages if value is given"""
        results = filter_prefs.get_result_list("language esp")
        self.assertEqual(results[0]["uid"], "yvs-language-spa")
        self.assertEqual(results[0]["title"], "Español (América Latina)")
        self.assertEqual(results[0].get("valid", True), True)
        self.assertEqual(len(results), 2)
        self.assertEqual(
            results[0]["variables"],
            {
                "pref_id": "language",
                "pref_name": "language",
                "value_id": '"spa"',
                "value_name": "Español (América Latina)",
            },
        )

    def test_filter_languages_non_latin(self):
        """should filter non-latin language names"""
        results = filter_prefs.get_result_list("language 繁")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["uid"], "yvs-language-zho_tw")
        self.assertEqual(results[0]["title"], "繁體中文")
        self.assertEqual(results[0].get("valid", True), True)
        self.assertEqual(
            results[0]["variables"],
            {
                "pref_id": "language",
                "pref_name": "language",
                "value_id": '"zho_tw"',
                "value_name": "繁體中文",
            },
        )

    @use_user_prefs(
        {"language": "spa", "version": 128, "refformat": "{name}\n{content}"}
    )
    def test_show_versions(self):
        """should show all versions if no value is given"""
        results = filter_prefs.get_result_list("version")
        self.assertGreater(len(results), 10)

    def test_filter_versions(self):
        """should filter available versions if value is given"""
        results = filter_prefs.get_result_list("version ni")
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["uid"], "yvs-version-110")
        self.assertEqual(
            results[0]["title"], "New International Reader’s Version (NIRV)"
        )
        self.assertEqual(results[0].get("valid", True), True)
        self.assertEqual(
            results[0]["variables"],
            {
                "pref_id": "version",
                "pref_name": "version",
                "value_id": "110",
                "value_name": "New International Reader’s Version (NIRV)",
            },
        )

    @use_user_prefs(
        {"language": "spa", "version": 128, "refformat": "{name}\n{content}"}
    )
    def test_show_refformats(self):
        """should show all refformats if no value is given"""
        results = filter_prefs.get_result_list("refformat")
        self.assertGreater(len(results), 3)

    def test_filter_refformats(self):
        """should filter available refformats if value is given"""
        results = filter_prefs.get_result_list("refformat http")
        result_title = '"Jesus wept." ¬ John 11:35 NIV ¬ {url}'.format(
            url=core.get_ref_url("111/jhn.11.35")
        )
        result_format_id = '"{content}"\n{name} {version}\n{url}'
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0]["uid"], "yvs-refformat-{id}".format(id=result_format_id)
        )
        self.assertEqual(results[0]["title"], result_title)
        self.assertEqual(results[0].get("valid", True), True)
        self.assertEqual(
            results[0]["variables"],
            {
                "pref_id": "refformat",
                "pref_name": "reference format",
                "value_id": json.dumps(result_format_id),
                "value_name": result_title,
            },
        )

    @use_user_prefs({"language": "eng", "version": 59, "refformat": "Z {content}"})
    def test_show_current_refformat(self):
        """should show current refformat as an available value"""
        results = filter_prefs.get_result_list("refformat Z")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["uid"], "yvs-refformat-Z {content}")
        self.assertEqual(results[0]["title"], "Z Jesus wept.")
        self.assertEqual(results[0]["valid"], False)
        self.assertEqual(
            results[0]["variables"],
            {
                "pref_id": "refformat",
                "pref_name": "reference format",
                "value_id": '"Z {content}"',
                "value_name": "Z Jesus wept.",
            },
        )

    def test_nonexistent_pref(self):
        """should not match nonexistent preference"""
        results = filter_prefs.get_result_list("xyz")
        self.assertEqual(len(results), 0)

    def test_nonexistent_value(self):
        """should return null result for nonexistent value"""
        results = filter_prefs.get_result_list("language xyz")
        self.assertRegex(results[0]["title"], "No Results")
        self.assertEqual(results[0]["valid"], False)
        self.assertEqual(len(results), 1)

    def test_current_value(self):
        """should not make preference's current value actionable"""
        results = filter_prefs.get_result_list("language english")
        self.assertEqual(results[0]["title"], "English")
        self.assertEqual(results[0]["valid"], False)
        self.assertEqual(len(results), 1)

    def test_invalid_query(self):
        """should show all available preferences for invalid preference name"""
        results = filter_prefs.get_result_list("!@#")
        self.assertNotEqual(len(results), 0)

    def test_show_all_preferences(self):
        """should show all available preferences if query is empty"""
        results = filter_prefs.get_result_list("")
        self.assertNotEqual(len(results), 0)

    def test_preferences_autocompletion(self):
        """autocompletion should be functioning for all preference results"""
        results = filter_prefs.get_result_list("")
        for result in results:
            self.assertIn("autocomplete", result)
            self.assertIn("valid", result)
            self.assertEqual(result["valid"], False)

    def test_filter_preferences_id(self):
        """should filter available preferences if partial pref ID is given"""
        results = filter_prefs.get_result_list("reff")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["uid"], "yvs-refformat")
        self.assertEqual(results[0]["title"], "Reference Format")

    def test_filter_preferences_name(self):
        """should filter available preferences if partial pref name is given"""
        results = filter_prefs.get_result_list("refe")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["uid"], "yvs-refformat")
        self.assertEqual(results[0]["title"], "Reference Format")

    def test_filter_preferences_name_partial(self):
        """should match partial pref name at word boundaries"""
        results = filter_prefs.get_result_list("version en sta v")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["uid"], "yvs-version-59")
        self.assertEqual(results[0]["title"], "English Standard Version 2016 (ESV)")

    def test_filter_preferences_show_current(self):
        """should show current values for all preferences"""
        results = filter_prefs.get_result_list("")
        self.assertEqual(len(results), 6)
        self.assertIn("English", results[0]["subtitle"])
        self.assertIn("NIV", results[1]["subtitle"])

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
    def test_filter_preferences_show_current_valid_only(self):
        """should not show invalid current preference values"""
        results = filter_prefs.get_result_list("")
        self.assertEqual(len(results), 6)
        self.assertIn("currently", results[0]["subtitle"])
        self.assertNotIn("currently", results[1]["subtitle"])

    def test_filter_preference_entire_query(self):
        """should match available preference values using entire query string"""
        results = filter_prefs.get_result_list("language español (españa)")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["uid"], "yvs-language-spa_es")
        self.assertEqual(results[0]["title"], "Español (España)")
        self.assertEqual(results[0].get("valid", True), True)
        self.assertEqual(
            results[0]["variables"],
            {
                "pref_id": "language",
                "pref_name": "language",
                "value_id": '"spa_es"',
                "value_name": "Español (España)",
            },
        )

    def test_filter_preference_ignore_special(self):
        """should ignore special characters when matching preference values"""
        results = filter_prefs.get_result_list("language 繁體中文$$")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["uid"], "yvs-language-zho_tw")
        self.assertEqual(results[0]["title"], "繁體中文")
        self.assertEqual(results[0].get("valid", True), True)
        self.assertEqual(
            results[0]["variables"],
            {
                "pref_id": "language",
                "pref_name": "language",
                "value_id": '"zho_tw"',
                "value_name": "繁體中文",
            },
        )

    @redirect_stdout
    def test_main_output(self, out):
        """should output pref result list JSON"""
        query_str = "language"
        filter_prefs.main(query_str)
        output = out.getvalue().rstrip()
        results = filter_prefs.get_result_list(query_str)
        feedback = core.get_result_list_feedback_str(results).rstrip()
        self.assertEqual(output, feedback)

    @redirect_stdout
    def test_null_result(self, out):
        """should output "No Results" JSON item for empty pref result list"""
        query_str = "xyz"
        filter_prefs.main(query_str)
        feedback_str = out.getvalue()
        feedback = json.loads(feedback_str)
        self.assertEqual(len(feedback["items"]), 1, "result item is missing")
        item = feedback["items"][0]
        self.assertEqual(item["title"], "No Results")
        self.assertEqual(item["valid"], False)

    @redirect_stdout
    def test_feedback_show_all(self, out):
        """should output JSON for all results if query is empty"""
        filter_prefs.main("")
        output = out.getvalue().rstrip()
        results = filter_prefs.get_result_list("")
        feedback = core.get_result_list_feedback_str(results).rstrip()
        self.assertEqual(output, feedback)
