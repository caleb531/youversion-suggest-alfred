#!/usr/bin/env python3
# coding=utf-8

import unittest

from nose2.tools.decorators import with_setup, with_teardown

import yvs.filter_refs as yvs
from tests import set_up, tear_down
from tests.decorators import use_user_prefs


case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
def test_book():
    """should recognize shorthand book syntax"""
    results = yvs.get_result_list('1co')
    case.assertEqual(results[0]['title'], '1 Corinthians 1 (NIV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_chapter():
    """should recognize shorthand chapter syntax"""
    results = yvs.get_result_list('1 co13')
    case.assertEqual(results[0]['title'], '1 Corinthians 13 (NIV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_version():
    """should recognize shorthand version syntax"""
    results = yvs.get_result_list('1 co 13esv')
    case.assertEqual(results[0]['title'], '1 Corinthians 13 (ESV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs({'language': 'zho_tw', 'version': 46, 'copybydefault': False})
def test_version_unicode():
    """should allow shorthand Unicode versions"""
    results = yvs.get_result_list('創世記1:3次經')
    case.assertEqual(results[0]['title'], '創世記 1:3 (次經)')
    case.assertEqual(len(results), 1)
