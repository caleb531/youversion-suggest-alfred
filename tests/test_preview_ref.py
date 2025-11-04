#!/usr/bin/env python3
# coding=utf-8

import json
import re
from unittest.mock import Mock, NonCallableMock, patch

import yvs.preview_ref as preview_ref
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


def test_preview_chapter():
    """should preview reference content for chapter"""

    with redirect_stdout() as out:
        preview_ref.main("111/psa.23")

    preview_feedback = json.loads(out.getvalue())

    assert not re.search("David", preview_feedback["response"])
    assert re.search("Lorem", preview_feedback["response"])
    assert re.search("nunc nulla", preview_feedback["response"])
    assert re.search("fermentum", preview_feedback["response"])
    assert "Psalms 23 (NIV)" in preview_feedback["footer"]


def test_preview_verse():
    """should preview reference content for verse"""

    with redirect_stdout() as out:
        preview_ref.main("59/psa.23.2")

    preview_feedback = json.loads(out.getvalue())

    assert not re.search("Lorem", preview_feedback["response"])
    assert re.search("nunc nulla", preview_feedback["response"])
    assert not re.search("fermentum", preview_feedback["response"])
    assert "Psalms 23:2 (ESV)" in preview_feedback["footer"]


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
def test_copybydefault_yes():
    """should display copy action when copybydefault is enabled"""

    with redirect_stdout() as out:
        preview_ref.main("59/psa.23.2")

    preview_feedback = json.loads(out.getvalue())

    assert "Copy content to clipboard" in preview_feedback["footer"]
    assert "View on YouVersion" not in preview_feedback["footer"]


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
def test_copybydefault_no():
    """should display view action when copybydefault is disabled"""

    with redirect_stdout() as out:
        preview_ref.main("59/psa.23.2")

    preview_feedback = json.loads(out.getvalue())

    assert "View on YouVersion" in preview_feedback["footer"]
    assert "Copy content to clipboard" not in preview_feedback["footer"]


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
def test_refformat():
    """should prefer Markdown refformat when generating preview"""

    with redirect_stdout() as out:
        preview_ref.main("59/psa.23.2")

    preview_feedback = json.loads(out.getvalue())

    assert "## Psalms 23:2 (ESV)  \n\n" in preview_feedback["response"]
    assert "- Psalms 23:2\n" not in preview_feedback["response"]
