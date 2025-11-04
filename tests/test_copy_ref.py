#!/usr/bin/env python3
# coding=utf-8

import json
import re
from unittest.mock import Mock, NonCallableMock, patch

import yvs.copy_ref as copy_ref
from tests.decorators import redirect_stdout, use_user_prefs

with open("tests/html/psa.23.html") as html_file:
    patch_urlopen = patch(
        "urllib.request.urlopen",
        return_value=NonCallableMock(read=Mock(return_value=html_file.read())),
    )


def setup_function(function):
    patch_urlopen.start()


def teardown_function(function):
    patch_urlopen.stop()


def test_copy_chapter():
    """should copy reference content for chapter"""

    ref_content = copy_ref.get_copied_ref("111/psa.23")

    assert not re.search("David", ref_content)
    assert re.search("Lorem", ref_content)
    assert re.search("nunc nulla", ref_content)
    assert re.search("fermentum", ref_content)


def test_copy_verse():
    """should copy reference content for verse"""

    ref_content = copy_ref.get_copied_ref("111/psa.23.2")

    assert not re.search("Lorem", ref_content)
    assert re.search("nunc nulla", ref_content)
    assert not re.search("fermentum", ref_content)


def test_copy_verse_range():
    """should copy reference content for verse range"""

    ref_content = copy_ref.get_copied_ref("111/psa.23.1-2")

    assert re.search("Lorem", ref_content)
    assert re.search("nunc nulla", ref_content)
    assert not re.search("fermentum", ref_content)


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

    ref_content = copy_ref.get_copied_ref("59/psa.23.6")

    assert ref_content == '"Proin nulla orci,"\n\n(Psalms 23:6 ESV)'


def test_header():
    """should prepend reference header to copied string"""

    ref_content = copy_ref.get_copied_ref("59/psa.23")

    assert re.search(r"^Psalms 23 \(ESV\)", ref_content)


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

    ref_content = copy_ref.get_copied_ref("128/psa.23")

    assert re.search(r"^Salmo 23 \(NVI\)", ref_content)


def test_whitespace_words():
    """should handle spaces appropriately"""

    ref_content = copy_ref.get_copied_ref("111/psa.23")

    assert re.search("adipiscing elit.", ref_content), (
        "should respect content consisting of spaces"
    )
    assert re.search("consectetur adipiscing", ref_content), (
        "should collapse consecutive spaces"
    )


def test_linebreaks_yes():
    """should add line breaks where appropriate"""

    ref_content = copy_ref.get_copied_ref("111/psa.23")

    assert re.search(
        r"Psalms 23 \(NIV\)\n\n\S",
        ref_content,
    ), "should add two line breaks after header"
    assert re.search(
        r"amet,\nconsectetur",
        ref_content,
    ), "should add newline before each p block"
    assert re.search(
        r"erat.\n\n\S",
        ref_content,
    ), "should add newline after each p block"
    assert re.search(
        r"orci,\ndapibus",
        ref_content,
    ), "should add newline between each qc block"
    assert re.search(
        r"nec\nfermentum",
        ref_content,
    ), "should add newline between each q block"
    assert re.search(
        r"elit.\n\nUt",
        ref_content,
    ), "should add newlines around each li1 block"
    assert re.search(
        r"leo,\n\nhendrerit",
        ref_content,
    ), "should add two newlines for each b block"


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

    ref_content = copy_ref.get_copied_ref("111/psa.23")

    assert re.search(
        r"Psalms 23 \(NIV\)\n\n\S",
        ref_content,
    ), "should still add two line breaks after header"
    assert re.search(
        r"amet, consectetur",
        ref_content,
    ), "should not add newline before each p block"
    assert re.search(
        r"erat. \S",
        ref_content,
    ), "should not add newline after each p block"
    assert re.search(
        r"orci, dapibus",
        ref_content,
    ), "should not add newline between each qc block"
    assert re.search(
        r"nec fermentum",
        ref_content,
    ), "should not add newline between each q block"
    assert re.search(
        r"elit. Ut",
        ref_content,
    ), "should not add newlines around each li1 block"
    assert re.search(
        r"leo, hendrerit",
        ref_content,
    ), "should not add two newlines for each b block"


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

    ref_content = copy_ref.get_copied_ref("111/psa.23")

    assert re.search(
        r"\(NIV\)\n\n1 » “Lorem ipsum”",
        ref_content,
    ), "should display number for verse 1"
    assert re.search(r"elit. 2 Ut", ref_content), "should display number for verse 2"
    assert re.search(
        r"erat. 3 › Nunc",
        ref_content,
    ), "should display number for verse 3"
    assert re.search(
        r"leo, 4 hendrerit",
        ref_content,
    ), "should display number for verse 4"
    assert re.search(
        r"nec 5 fermentum",
        ref_content,
    ), "should display number for verse 5"
    assert re.search(
        r"orci, 7-9 dapibus",
        ref_content,
    ), "should display number for verses 7-9"
    assert re.search(
        r"augue in, 10 dictum",
        ref_content,
    ), "should display number for verse 10"


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

    ref_content = copy_ref.get_copied_ref("111/psa.23")

    assert re.search(r"5 fermentum", ref_content)
    assert not re.search(r"#", ref_content)


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

    ref_content = copy_ref.get_copied_ref("111/psa.23.7-9")

    assert re.search(r"7-9 dapibus et augue in,", ref_content)
    assert not re.search(r"#", ref_content)
    assert not re.search(r"\b(1|2|3|4|5|6|10)\b", ref_content)


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

    ref_content = copy_ref.get_copied_ref("111/psa.23.7")

    assert re.search(r"7-9 dapibus et augue in,", ref_content)
    assert not re.search(r"#", ref_content)


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

    ref_content = copy_ref.get_copied_ref("111/psa.23.9")

    assert re.search(r"7-9 dapibus et augue in,", ref_content)
    assert not re.search(r"#", ref_content)


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

    ref_content = copy_ref.get_copied_ref("111/psa.23.8")

    assert re.search(r"7-9 dapibus et augue in,", ref_content)
    assert not re.search(r"#", ref_content)


@patch("yvs.web.get_url_content", return_value="abc")
def test_url_always_chapter(get_url_content):
    """should always fetch HTML from chapter URL"""

    copy_ref.get_copied_ref("59/psa.23.2")

    get_url_content.assert_called_with("https://www.bible.com/bible/59/PSA.23")


def test_cache_url_content():
    """should cache chapter URL content after first fetch"""

    copy_ref.get_copied_ref("59/psa.23.2")

    with patch("urllib.request.Request") as request:
        copy_ref.get_copied_ref("59/psa.23.3")
        request.assert_not_called()


def test_nonexistent_verse():
    """should return empty string for nonexistent verses"""

    ref_content = copy_ref.get_copied_ref("111/psa.23.13")

    assert ref_content == ""


def test_unicode_content():
    """should return copied reference content as Unicode"""

    ref_content = copy_ref.get_copied_ref("111/psa.23")

    assert isinstance(ref_content, str)


@patch("yvs.cache.get_cache_entry_content", return_value="<a>")
@patch("yvs.web.get_url_content", side_effect=copy_ref.web.get_url_content)
def test_revalidate(get_cache_entry_content, get_url_content):
    """should re-fetch latest HTML when cached HTML can no longer be parsed"""

    ref_content = copy_ref.get_copied_ref("111/psa.23.1")

    assert ref_content != ""
    assert get_url_content.call_count == 1


def test_main():
    """main function should output copied reference content"""

    ref_uid = "59/psa.23"
    ref_content = copy_ref.get_copied_ref(ref_uid)

    with redirect_stdout() as out:
        copy_ref.main(ref_uid)

    main_json = json.loads(out.getvalue())
    assert main_json == {
        "alfredworkflow": {
            "arg": ref_uid,
            "variables": {
                "copied_ref": ref_content,
                "full_ref_name": "Psalms 23 (ESV)",
            },
        }
    }
