#!/usr/bin/env python

import nose.tools as nose
import yv_suggest.search as yvs


def test_empty():
    """should not match empty input"""
    results = yvs.get_result_list('')
    nose.assert_equal(len(results), 0)


def test_invalid():
    """should not match invalid input"""
    results = yvs.get_result_list('!!!')
    nose.assert_equal(len(results), 0)


def test_invalid_xml():
    """should not match input containing XML reserved characters"""
    results = yvs.get_result_list('<input>')
    nose.assert_equal(len(results), 0)
