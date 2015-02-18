#!/usr/bin/env python

import nose.tools as nose
import yv_suggest.search as yvs


def test_incomplete_verse():
    """should treat incomplete verse reference as chapter reference"""
    results = yvs.get_result_list('psalm 19:')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Psalm 19 (NIV)')


def test_incomplete_dot_verse():
    """should treat incomplete .verse reference as chapter reference"""
    results = yvs.get_result_list('psalm 19.')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Psalm 19 (NIV)')


def test_incomplete_verse_range():
    """should treat incomplete verse ranges as single-verse references"""
    results = yvs.get_result_list('psalm 19.7-')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Psalm 19:7 (NIV)')
