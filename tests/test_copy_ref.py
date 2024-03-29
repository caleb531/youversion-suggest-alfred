#!/usr/bin/env python3
# coding=utf-8

import json
import unittest
from unittest.mock import Mock, NonCallableMock, patch

from nose2.tools.decorators import with_setup, with_teardown

import tests
import yvs.copy_ref as yvs
from tests.decorators import redirect_stdout, use_user_prefs

case = unittest.TestCase()

with open("tests/html/psa.23.html") as html_file:
    patch_urlopen = patch(
        "urllib.request.urlopen",
        return_value=NonCallableMock(read=Mock(return_value=html_file.read())),
    )


def set_up():
    patch_urlopen.start()
    tests.set_up()


def tear_down():
    patch_urlopen.stop()
    tests.tear_down()


@with_setup(set_up)
@with_teardown(tear_down)
def test_copy_chapter():
    """should copy reference content for chapter"""
    ref_content = yvs.get_copied_ref("111/psa.23")
    case.assertNotRegex(ref_content, "David")
    case.assertRegex(ref_content, "Lorem")
    case.assertRegex(ref_content, "nunc nulla")
    case.assertRegex(ref_content, "fermentum")


@with_setup(set_up)
@with_teardown(tear_down)
def test_copy_verse():
    """should copy reference content for verse"""
    ref_content = yvs.get_copied_ref("111/psa.23.2")
    case.assertNotRegex(ref_content, "Lorem")
    case.assertRegex(ref_content, "nunc nulla")
    case.assertNotRegex(ref_content, "fermentum")


@with_setup(set_up)
@with_teardown(tear_down)
def test_copy_verse_range():
    """should copy reference content for verse range"""
    ref_content = yvs.get_copied_ref("111/psa.23.1-2")
    case.assertRegex(ref_content, "Lorem")
    case.assertRegex(ref_content, "nunc nulla")
    case.assertNotRegex(ref_content, "fermentum")


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs(
    {
        "language": "eng",
        "version": 59,
        "refformat": '"{content}"\n\n({name} {version})',
        "versenumbers": False,
        "linebreaks": True,
    }
)
def test_refformat():
    """should honor the chosen reference format"""
    ref_content = yvs.get_copied_ref("59/psa.23.6")
    case.assertEqual(ref_content, '"Proin nulla orci,"\n\n(Psalms 23:6 ESV)')


@with_setup(set_up)
@with_teardown(tear_down)
def test_header():
    """should prepend reference header to copied string"""
    ref_content = yvs.get_copied_ref("59/psa.23")
    case.assertRegex(ref_content, r"^Psalms 23 \(ESV\)")


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs(
    {
        "language": "spa",
        "version": 128,
        "refformat": "{name} ({version})\n\n{content}",
        "versenumbers": False,
        "linebreaks": True,
    }
)
def test_header_language():
    """reference header should reflect chosen language"""
    ref_content = yvs.get_copied_ref("128/psa.23")
    case.assertRegex(ref_content, r"^Salmo 23 \(NVI\)")


@with_setup(set_up)
@with_teardown(tear_down)
def test_whitespace_words():
    """should handle spaces appropriately"""
    ref_content = yvs.get_copied_ref("111/psa.23")
    case.assertRegex(
        ref_content, "adipiscing elit.", "should respect content consisting of spaces"
    )
    case.assertRegex(
        ref_content, "consectetur adipiscing", "should collapse consecutive spaces"
    )


@with_setup(set_up)
@with_teardown(tear_down)
def test_linebreaks_yes():
    """should add line breaks where appropriate"""
    ref_content = yvs.get_copied_ref("111/psa.23")
    case.assertRegex(
        ref_content,
        r"Psalms 23 \(NIV\)\n\n\S",
        "should add two line breaks after header",
    )
    case.assertRegex(
        ref_content, r"amet,\nconsectetur", "should add newline before each p block"
    )
    case.assertRegex(
        ref_content, r"erat.\n\n\S", "should add newline after each p block"
    )
    case.assertRegex(
        ref_content, r"orci,\ndapibus", "should add newline between each qc block"
    )
    case.assertRegex(
        ref_content, r"nec\nfermentum", "should add newline between each q block"
    )
    case.assertRegex(
        ref_content, r"elit.\n\nUt", "should add newlines around each li1 block"
    )
    case.assertRegex(
        ref_content, r"leo,\n\nhendrerit", "should add two newlines for each b block"
    )


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs(
    {
        "language": "eng",
        "version": 111,
        "refformat": "{name} ({version})\n\n{content}",
        "versenumbers": False,
        "linebreaks": False,
    }
)
def test_linebreaks_no():
    """should strip line breaks where appropriate"""
    ref_content = yvs.get_copied_ref("111/psa.23")
    case.assertRegex(
        ref_content,
        r"Psalms 23 \(NIV\)\n\n\S",
        "should still add two line breaks after header",
    )
    case.assertRegex(
        ref_content, r"amet, consectetur", "should not add newline before each p block"
    )
    case.assertRegex(
        ref_content, r"erat. \S", "should not add newline after each p block"
    )
    case.assertRegex(
        ref_content, r"orci, dapibus", "should not add newline between each qc block"
    )
    case.assertRegex(
        ref_content, r"nec fermentum", "should not add newline between each q block"
    )
    case.assertRegex(
        ref_content, r"elit. Ut", "should not add newlines around each li1 block"
    )
    case.assertRegex(
        ref_content, r"leo, hendrerit", "should not add two newlines for each b block"
    )


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs(
    {
        "language": "eng",
        "version": 111,
        "refformat": "{name} ({version})\n\n{content}",
        "versenumbers": True,
        "linebreaks": False,
    }
)
def test_linebreaks_no_versenumbers_yes():
    """should display verse numbers correctly when stripping line breaks"""
    ref_content = yvs.get_copied_ref("111/psa.23")
    case.assertRegex(
        ref_content,
        r"\(NIV\)\n\n1 » “Lorem ipsum”",
        "should display number for verse 1",
    )
    case.assertRegex(ref_content, r"elit. 2 Ut", "should display number for verse 2")
    case.assertRegex(
        ref_content, r"erat. 3 › Nunc", "should display number for verse 3"
    )
    case.assertRegex(
        ref_content, r"leo, 4 hendrerit", "should display number for verse 4"
    )
    case.assertRegex(
        ref_content, r"leo, 4 hendrerit", "should display number for verse 4"
    )
    case.assertRegex(
        ref_content, r"nec 5 fermentum", "should display number for verse 5"
    )
    case.assertRegex(
        ref_content, r"orci, 7-9 dapibus", "should display number for verses 7-9"
    )
    case.assertRegex(
        ref_content, r"augue in, 10 dictum", "should display number for verse 10"
    )


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs(
    {
        "language": "eng",
        "version": 111,
        "refformat": "{name} ({version})\n\n{content}",
        "versenumbers": True,
        "linebreaks": True,
    }
)
def test_versenumbers():
    """should honor the versenumbers preference"""
    ref_content = yvs.get_copied_ref("111/psa.23")
    case.assertRegex(ref_content, r"5 fermentum")
    case.assertNotRegex(ref_content, r"#")


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs(
    {
        "language": "eng",
        "version": 97,
        "refformat": "{name} ({version})\n\n{content}",
        "versenumbers": True,
        "linebreaks": True,
    }
)
def test_versenumbers_range():
    """should handle verse range labels (used by versions like the MSG)"""
    ref_content = yvs.get_copied_ref("111/psa.23.7-9")
    case.assertRegex(ref_content, r"7-9 dapibus et augue in,")
    case.assertNotRegex(ref_content, r"#")


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs(
    {
        "language": "eng",
        "version": 97,
        "refformat": "{name} ({version})\n\n{content}",
        "versenumbers": True,
        "linebreaks": True,
    }
)
def test_versenumbers_range_start():
    """should handle range labels when verse at start of range is given"""
    ref_content = yvs.get_copied_ref("111/psa.23.7")
    case.assertRegex(ref_content, r"7-9 dapibus et augue in,")
    case.assertNotRegex(ref_content, r"#")


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs(
    {
        "language": "eng",
        "version": 97,
        "refformat": "{name} ({version})\n\n{content}",
        "versenumbers": True,
        "linebreaks": True,
    }
)
def test_versenumbers_range_end():
    """should handle range labels when verse at end of range is given"""
    ref_content = yvs.get_copied_ref("111/psa.23.9")
    case.assertRegex(ref_content, r"7-9 dapibus et augue in,")
    case.assertNotRegex(ref_content, r"#")


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs(
    {
        "language": "eng",
        "version": 97,
        "refformat": "{name} ({version})\n\n{content}",
        "versenumbers": True,
        "linebreaks": True,
    }
)
def test_versenumbers_range_middle():
    """should handle range labels when verse in middle of range is given"""
    ref_content = yvs.get_copied_ref("111/psa.23.8")
    case.assertRegex(ref_content, r"7-9 dapibus et augue in,")
    case.assertNotRegex(ref_content, r"#")


@with_setup(set_up)
@with_teardown(tear_down)
@patch("yvs.web.get_url_content", return_value="abc")
def test_url_always_chapter(get_url_content):
    """should always fetch HTML from chapter URL"""
    yvs.get_copied_ref("59/psa.23.2")
    get_url_content.assert_called_with("https://www.bible.com/bible/59/PSA.23")


@with_setup(set_up)
@with_teardown(tear_down)
def test_cache_url_content():
    """should cache chapter URL content after first fetch"""
    yvs.get_copied_ref("59/psa.23.2")
    with patch("urllib.request.Request") as request:
        yvs.get_copied_ref("59/psa.23.3")
        request.assert_not_called()


@with_setup(set_up)
@with_teardown(tear_down)
def test_nonexistent_verse():
    """should return empty string for nonexistent verses"""
    ref_content = yvs.get_copied_ref("111/psa.23.13")
    case.assertEqual(ref_content, "")


@with_setup(set_up)
@with_teardown(tear_down)
def test_unicode_content():
    """should return copied reference content as Unicode"""
    ref_content = yvs.get_copied_ref("111/psa.23")
    case.assertIsInstance(ref_content, str)


@with_setup(set_up)
@with_teardown(tear_down)
@patch("yvs.cache.get_cache_entry_content", return_value="<a>")
@patch("yvs.web.get_url_content", side_effect=yvs.web.get_url_content)
def test_revalidate(get_cache_entry_content, get_url_content):
    """should re-fetch latest HTML when cached HTML can no longer be parsed"""
    ref_content = yvs.get_copied_ref("111/psa.23.1")
    case.assertNotEqual(ref_content, "")
    case.assertEqual(get_url_content.call_count, 1)


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_main(out):
    """main function should output copied reference content"""
    ref_uid = "59/psa.23"
    ref_content = yvs.get_copied_ref(ref_uid)
    yvs.main(ref_uid)
    main_json = json.loads(out.getvalue())
    case.assertEqual(
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
