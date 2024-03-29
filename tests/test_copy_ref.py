#!/usr/bin/env python3
# coding=utf-8

import json
from unittest.mock import Mock, NonCallableMock, patch

import yvs.copy_ref as yvs
from tests import YVSTestCase
from tests.decorators import redirect_stdout, use_user_prefs

with open("tests/html/psa.23.html") as html_file:
    patch_urlopen = patch(
        "urllib.request.urlopen",
        return_value=NonCallableMock(read=Mock(return_value=html_file.read())),
    )


class TestCopyRef(YVSTestCase):

    def setUp(self):
        patch_urlopen.start()
        super().setUp()

    def tearDown(self):
        patch_urlopen.stop()
        super().tearDown()

    def test_copy_chapter(self):
        """should copy reference content for chapter"""
        ref_content = yvs.get_copied_ref("111/psa.23")
        self.assertNotRegex(ref_content, "David")
        self.assertRegex(ref_content, "Lorem")
        self.assertRegex(ref_content, "nunc nulla")
        self.assertRegex(ref_content, "fermentum")

    def test_copy_verse(self):
        """should copy reference content for verse"""
        ref_content = yvs.get_copied_ref("111/psa.23.2")
        self.assertNotRegex(ref_content, "Lorem")
        self.assertRegex(ref_content, "nunc nulla")
        self.assertNotRegex(ref_content, "fermentum")

    def test_copy_verse_range(self):
        """should copy reference content for verse range"""
        ref_content = yvs.get_copied_ref("111/psa.23.1-2")
        self.assertRegex(ref_content, "Lorem")
        self.assertRegex(ref_content, "nunc nulla")
        self.assertNotRegex(ref_content, "fermentum")

    @use_user_prefs(
        {
            "language": "eng",
            "version": 59,
            "refformat": '"{content}"\n\n({name} {version})',
            "versenumbers": False,
            "linebreaks": True,
        }
    )
    def test_refformat(self):
        """should honor the chosen reference format"""
        ref_content = yvs.get_copied_ref("59/psa.23.6")
        self.assertEqual(ref_content, '"Proin nulla orci,"\n\n(Psalms 23:6 ESV)')

    def test_header(self):
        """should prepend reference header to copied string"""
        ref_content = yvs.get_copied_ref("59/psa.23")
        self.assertRegex(ref_content, r"^Psalms 23 \(ESV\)")

    @use_user_prefs(
        {
            "language": "spa",
            "version": 128,
            "refformat": "{name} ({version})\n\n{content}",
            "versenumbers": False,
            "linebreaks": True,
        }
    )
    def test_header_language(self):
        """reference header should reflect chosen language"""
        ref_content = yvs.get_copied_ref("128/psa.23")
        self.assertRegex(ref_content, r"^Salmo 23 \(NVI\)")

    def test_whitespace_words(self):
        """should handle spaces appropriately"""
        ref_content = yvs.get_copied_ref("111/psa.23")
        self.assertRegex(
            ref_content,
            "adipiscing elit.",
            "should respect content consisting of spaces",
        )
        self.assertRegex(
            ref_content, "consectetur adipiscing", "should collapse consecutive spaces"
        )

    def test_linebreaks_yes(self):
        """should add line breaks where appropriate"""
        ref_content = yvs.get_copied_ref("111/psa.23")
        self.assertRegex(
            ref_content,
            r"Psalms 23 \(NIV\)\n\n\S",
            "should add two line breaks after header",
        )
        self.assertRegex(
            ref_content, r"amet,\nconsectetur", "should add newline before each p block"
        )
        self.assertRegex(
            ref_content, r"erat.\n\n\S", "should add newline after each p block"
        )
        self.assertRegex(
            ref_content, r"orci,\ndapibus", "should add newline between each qc block"
        )
        self.assertRegex(
            ref_content, r"nec\nfermentum", "should add newline between each q block"
        )
        self.assertRegex(
            ref_content, r"elit.\n\nUt", "should add newlines around each li1 block"
        )
        self.assertRegex(
            ref_content,
            r"leo,\n\nhendrerit",
            "should add two newlines for each b block",
        )

    @use_user_prefs(
        {
            "language": "eng",
            "version": 111,
            "refformat": "{name} ({version})\n\n{content}",
            "versenumbers": False,
            "linebreaks": False,
        }
    )
    def test_linebreaks_no(self):
        """should strip line breaks where appropriate"""
        ref_content = yvs.get_copied_ref("111/psa.23")
        self.assertRegex(
            ref_content,
            r"Psalms 23 \(NIV\)\n\n\S",
            "should still add two line breaks after header",
        )
        self.assertRegex(
            ref_content,
            r"amet, consectetur",
            "should not add newline before each p block",
        )
        self.assertRegex(
            ref_content, r"erat. \S", "should not add newline after each p block"
        )
        self.assertRegex(
            ref_content,
            r"orci, dapibus",
            "should not add newline between each qc block",
        )
        self.assertRegex(
            ref_content, r"nec fermentum", "should not add newline between each q block"
        )
        self.assertRegex(
            ref_content, r"elit. Ut", "should not add newlines around each li1 block"
        )
        self.assertRegex(
            ref_content,
            r"leo, hendrerit",
            "should not add two newlines for each b block",
        )

    @use_user_prefs(
        {
            "language": "eng",
            "version": 111,
            "refformat": "{name} ({version})\n\n{content}",
            "versenumbers": True,
            "linebreaks": False,
        }
    )
    def test_linebreaks_no_versenumbers_yes(self):
        """should display verse numbers correctly when stripping line breaks"""
        ref_content = yvs.get_copied_ref("111/psa.23")
        self.assertRegex(
            ref_content,
            r"\(NIV\)\n\n1 » “Lorem ipsum”",
            "should display number for verse 1",
        )
        self.assertRegex(
            ref_content, r"elit. 2 Ut", "should display number for verse 2"
        )
        self.assertRegex(
            ref_content, r"erat. 3 › Nunc", "should display number for verse 3"
        )
        self.assertRegex(
            ref_content, r"leo, 4 hendrerit", "should display number for verse 4"
        )
        self.assertRegex(
            ref_content, r"leo, 4 hendrerit", "should display number for verse 4"
        )
        self.assertRegex(
            ref_content, r"nec 5 fermentum", "should display number for verse 5"
        )
        self.assertRegex(
            ref_content, r"orci, 7-9 dapibus", "should display number for verses 7-9"
        )
        self.assertRegex(
            ref_content, r"augue in, 10 dictum", "should display number for verse 10"
        )

    @use_user_prefs(
        {
            "language": "eng",
            "version": 111,
            "refformat": "{name} ({version})\n\n{content}",
            "versenumbers": True,
            "linebreaks": True,
        }
    )
    def test_versenumbers(self):
        """should honor the versenumbers preference"""
        ref_content = yvs.get_copied_ref("111/psa.23")
        self.assertRegex(ref_content, r"5 fermentum")
        self.assertNotRegex(ref_content, r"#")

    @use_user_prefs(
        {
            "language": "eng",
            "version": 97,
            "refformat": "{name} ({version})\n\n{content}",
            "versenumbers": True,
            "linebreaks": True,
        }
    )
    def test_versenumbers_range(self):
        """should handle verse range labels (used by versions like the MSG)"""
        ref_content = yvs.get_copied_ref("111/psa.23.7-9")
        self.assertRegex(ref_content, r"7-9 dapibus et augue in,")
        self.assertNotRegex(ref_content, r"#")

    @use_user_prefs(
        {
            "language": "eng",
            "version": 97,
            "refformat": "{name} ({version})\n\n{content}",
            "versenumbers": True,
            "linebreaks": True,
        }
    )
    def test_versenumbers_range_start(self):
        """should handle range labels when verse at start of range is given"""
        ref_content = yvs.get_copied_ref("111/psa.23.7")
        self.assertRegex(ref_content, r"7-9 dapibus et augue in,")
        self.assertNotRegex(ref_content, r"#")

    @use_user_prefs(
        {
            "language": "eng",
            "version": 97,
            "refformat": "{name} ({version})\n\n{content}",
            "versenumbers": True,
            "linebreaks": True,
        }
    )
    def test_versenumbers_range_end(self):
        """should handle range labels when verse at end of range is given"""
        ref_content = yvs.get_copied_ref("111/psa.23.9")
        self.assertRegex(ref_content, r"7-9 dapibus et augue in,")
        self.assertNotRegex(ref_content, r"#")

    @use_user_prefs(
        {
            "language": "eng",
            "version": 97,
            "refformat": "{name} ({version})\n\n{content}",
            "versenumbers": True,
            "linebreaks": True,
        }
    )
    def test_versenumbers_range_middle(self):
        """should handle range labels when verse in middle of range is given"""
        ref_content = yvs.get_copied_ref("111/psa.23.8")
        self.assertRegex(ref_content, r"7-9 dapibus et augue in,")
        self.assertNotRegex(ref_content, r"#")

    @patch("yvs.web.get_url_content", return_value="abc")
    def test_url_always_chapter(self, get_url_content):
        """should always fetch HTML from chapter URL"""
        yvs.get_copied_ref("59/psa.23.2")
        get_url_content.assert_called_with("https://www.bible.com/bible/59/PSA.23")

    def test_cache_url_content(self):
        """should cache chapter URL content after first fetch"""
        yvs.get_copied_ref("59/psa.23.2")
        with patch("urllib.request.Request") as request:
            yvs.get_copied_ref("59/psa.23.3")
            request.assert_not_called()

    def test_nonexistent_verse(self):
        """should return empty string for nonexistent verses"""
        ref_content = yvs.get_copied_ref("111/psa.23.13")
        self.assertEqual(ref_content, "")

    def test_unicode_content(self):
        """should return copied reference content as Unicode"""
        ref_content = yvs.get_copied_ref("111/psa.23")
        self.assertIsInstance(ref_content, str)

    @patch("yvs.cache.get_cache_entry_content", return_value="<a>")
    @patch("yvs.web.get_url_content", side_effect=yvs.web.get_url_content)
    def test_revalidate(self, get_cache_entry_content, get_url_content):
        """should re-fetch latest HTML when cached HTML can no longer be parsed"""
        ref_content = yvs.get_copied_ref("111/psa.23.1")
        self.assertNotEqual(ref_content, "")
        self.assertEqual(get_url_content.call_count, 1)

    @redirect_stdout
    def test_main(self, out):
        """main function should output copied reference content"""
        ref_uid = "59/psa.23"
        ref_content = yvs.get_copied_ref(ref_uid)
        yvs.main(ref_uid)
        main_json = json.loads(out.getvalue())
        self.assertEqual(
            main_json,
            {
                "alfredworkflow": {
                    "arg": ref_uid,
                    "variables": {
                        "copied_ref": ref_content,
                        "full_ref_name": "Psalms 23 (ESV)",
                    },
                }
            },
        )
