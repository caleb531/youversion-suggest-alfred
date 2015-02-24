#!/usr/bin/env python

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.search as yvs


def test_book():
    """should recognize shorthand book syntax"""
    results = yvs.get_result_list('1co')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], '1 Corinthians 1 (NIV)')


def test_chapter():
    """should recognize shorthand chapter syntax"""
    results = yvs.get_result_list('1 co13')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], '1 Corinthians 13 (NIV)')


def test_version():
    """should recognize shorthand version syntax"""
    results = yvs.get_result_list('1 co 13esv')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], '1 Corinthians 13 (ESV)')
