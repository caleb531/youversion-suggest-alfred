#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.search as yvs


def test_whitespace():
    """should match references irrespective of surrounding whitespace"""
    results = yvs.get_result_list('  romans  8  28  a  ')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Romans 8:28 (AMP)')


def test_littered():
    """should match reference literred with non-alphanumeric characters"""
    results = yvs.get_result_list('1!co@13#4$7^e')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], '1 Corinthians 13:4-7 (ESV)')


def test_unicode_accented():
    """should remove accents from accented characters"""
    results = yvs.get_result_list('é')
    nose.assert_equal(len(results), 6)


def test_unicode_obscure():
    """should recognize extended Unicode characters"""
    results = yvs.get_result_list('π')
    nose.assert_equal(len(results), 0)
