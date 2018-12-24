# tests.test_filter_refs.test_incomplete

from __future__ import print_function, unicode_literals

import nose.tools as nose

import yvs.filter_refs as yvs
from tests import set_up, tear_down


@nose.with_setup(set_up, tear_down)
def test_incomplete_verse():
    """should treat incomplete verse reference as chapter reference"""
    results = yvs.get_result_list('psalm 19:')
    nose.assert_equal(results[0]['title'], 'Psalm 19 (NIV)')
    nose.assert_equal(len(results), 1)


@nose.with_setup(set_up, tear_down)
def test_incomplete_dot_verse():
    """should treat incomplete .verse reference as chapter reference"""
    results = yvs.get_result_list('psalm 19.')
    nose.assert_equal(results[0]['title'], 'Psalm 19 (NIV)')
    nose.assert_equal(len(results), 1)


@nose.with_setup(set_up, tear_down)
def test_incomplete_verse_range():
    """should treat incomplete verse ranges as single-verse references"""
    results = yvs.get_result_list('psalm 19.7-')
    nose.assert_equal(results[0]['title'], 'Psalm 19:7 (NIV)')
    nose.assert_equal(len(results), 1)
