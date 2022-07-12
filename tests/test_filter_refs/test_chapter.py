#!/usr/bin/env python3
# coding=utf-8

import unittest

from nose2.tools.decorators import with_setup, with_teardown

import yvs.filter_refs as yvs
from tests import set_up, tear_down


case = unittest.TestCase()


@with_setup(set_up)
@with_teardown(tear_down)
def test_basic():
    """should match chapters"""
    results = yvs.get_result_list('matthew 5')
    case.assertEqual(results[0]['title'], 'Matthew 5 (NIV)')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_ambiguous():
    """should match chapters by ambiguous book name"""
    results = yvs.get_result_list('a 3')
    case.assertEqual(results[0]['title'], 'Amos 3 (NIV)')
    case.assertEqual(results[1]['title'], 'Acts 3 (NIV)')
    case.assertEqual(len(results), 2)


@with_setup(set_up)
@with_teardown(tear_down)
def test_id():
    """should use correct ID for chapters"""
    results = yvs.get_result_list('luke 4')
    case.assertEqual(results[0]['uid'], 'yvs-111/luk.4')
    case.assertEqual(len(results), 1)


@with_setup(set_up)
@with_teardown(tear_down)
def test_zero_chapter():
    """should interpret chapter zero as chapter one"""
    results = yvs.get_result_list('ps 0')
    case.assertEqual(results[0]['title'], 'Psalms 1 (NIV)')
    case.assertEqual(len(results), 1)
