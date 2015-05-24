#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.filter_refs as yvs


def test_whitespace():
    """should ignore excessive whitespace"""
    results = yvs.get_result_list('  romans  8  28  a  ', prefs={})
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Romans 8:28 (AMP)')


def test_littered():
    """should ignore non-alphanumeric characters"""
    results = yvs.get_result_list('!1@co#13$4^7&e*', prefs={})
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], '1 Corinthians 13:4-7 (ESV)')


def test_trailing_alphanumeric():
    """should ignore trailing non-matching alphanumeric characters"""
    results = yvs.get_result_list('2 co 3 x y z 1 2 3', prefs={})
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], '2 Corinthians 3 (NIV)')


def test_unicode_accented():
    """should recognize accented Unicode characters"""
    results = yvs.get_result_list('é 3', prefs={
        'language': 'es'
    })
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Éxodo 3 (NVI)')


def test_unicode_normalization():
    """should normalize Unicode characters"""
    results = yvs.get_result_list('e\u0301', prefs={})
    nose.assert_equal(len(results), 0)
