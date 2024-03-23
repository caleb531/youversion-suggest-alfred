#!/usr/bin/env python3
# coding=utf-8

import json
import unittest
from unittest.mock import Mock, NonCallableMock, patch

from nose2.tools.decorators import with_setup, with_teardown

import tests
import yvs.preview_ref as yvs
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
@redirect_stdout
def test_preview_chapter(out):
    """should preview reference content for chapter"""
    yvs.main("111/psa.23")
    preview_feedback = json.loads(out.getvalue())
    case.assertNotRegex(preview_feedback["response"], "David")
    case.assertRegex(preview_feedback["response"], "Lorem")
    case.assertRegex(preview_feedback["response"], "nunc nulla")
    case.assertRegex(preview_feedback["response"], "fermentum")
    case.assertIn("Psalms 23 (NIV)", preview_feedback["footer"])


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_preview_verse(out):
    """should preview reference content for verse"""
    yvs.main("59/psa.23.2")
    preview_feedback = json.loads(out.getvalue())
    case.assertNotRegex(preview_feedback["response"], "Lorem")
    case.assertRegex(preview_feedback["response"], "nunc nulla")
    case.assertNotRegex(preview_feedback["response"], "fermentum")
    case.assertIn("Psalms 23:2 (ESV)", preview_feedback["footer"])


@with_setup(set_up)
@with_teardown(tear_down)
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
def test_copybydefault_yes(out):
    """should display copy action when copybydefault is enabled"""
    yvs.main("59/psa.23.2")
    preview_feedback = json.loads(out.getvalue())
    case.assertIn("Copy content to clipboard", preview_feedback["footer"])
    case.assertNotIn("View on YouVersion", preview_feedback["footer"])


@with_setup(set_up)
@with_teardown(tear_down)
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
def test_copybydefault_no(out):
    """should display view action when copybydefault is disabled"""
    yvs.main("59/psa.23.2")
    preview_feedback = json.loads(out.getvalue())
    case.assertIn("View on YouVersion", preview_feedback["footer"])
    case.assertNotIn("Copy content to clipboard", preview_feedback["footer"])


@with_setup(set_up)
@with_teardown(tear_down)
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
def test_refformat(out):
    """
    should bypass user's refformat and use consistent refformat for preview
    """
    yvs.main("59/psa.23.2")
    preview_feedback = json.loads(out.getvalue())
    case.assertIn("Psalms 23:2 (ESV)\n\n", preview_feedback["response"])
    case.assertNotIn("- Psalms 23:2\n", preview_feedback["response"])
