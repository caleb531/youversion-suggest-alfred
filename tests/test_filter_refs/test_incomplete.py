#!/usr/bin/env python3
# coding=utf-8

import unittest

from nose2.tools.decorators import with_setup, with_teardown

import yvs.filter_refs as yvs
from tests import set_up, tear_down


case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
def test_incomplete_verse():
    """should treat incomplete verse reference as chapter reference"""
    results = yvs.get_result_list('Psalms 19:')
    case.assertEqual(results[0]['title'], 'Psalms 19 (NIV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_incomplete_dot_verse():
    """should treat incomplete .verse reference as chapter reference"""
    results = yvs.get_result_list('Psalms 19.')
    case.assertEqual(results[0]['title'], 'Psalms 19 (NIV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_incomplete_verse_range():
    """should treat incomplete verse ranges as single-verse references"""
    results = yvs.get_result_list('Psalms 19.7-')
    case.assertEqual(results[0]['title'], 'Psalms 19:7 (NIV)')
    case.assertEqual(len(results), 1)
