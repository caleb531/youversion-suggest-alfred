#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.filter_prefs as yvs
from xml.etree import ElementTree as ET
import context_managers as ctx


def test_show_languages():
    """should show all languages if no value is given"""
    results = yvs.get_result_list('language', prefs={})
    nose.assert_not_equal(len(results), 0)


def test_filter_languages():
    """should filter available languages if value is given"""
    results = yvs.get_result_list('language en', prefs={})
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'English')
    nose.assert_equal(results[0]['arg'], 'language:en')


def test_show_versions():
    """should show all versions if no value is given"""
    results = yvs.get_result_list('version', prefs={})
    nose.assert_not_equal(len(results), 0)


def test_filter_versions():
    """should filter available versions if value is given"""
    results = yvs.get_result_list('version ni', prefs={})
    nose.assert_equal(len(results), 3)
    nose.assert_equal(results[0]['title'], 'NIRV')
    nose.assert_equal(results[0]['arg'], 'version:110')


def test_nonexistent():
    """should not match nonexistent preference"""
    results = yvs.get_result_list('xyz', prefs={})
    nose.assert_equal(len(results), 0)


def test_invalid():
    """should not match nonexistent preference"""
    results = yvs.get_result_list('!@#', prefs={})
    nose.assert_equal(len(results), 0)


def test_main_output():
    """should output pref result list XML"""
    query_str = 'language'
    with ctx.redirect_stdout() as out:
        yvs.main(query_str, prefs={})
        output = out.getvalue().strip()
        results = yvs.get_result_list(query_str, prefs={})
        xml = yvs.shared.get_result_list_xml(results).strip()
        nose.assert_equal(output, xml)


def test_null_result():
    """should output "No Results" XML item for empty pref result list"""
    query_str = 'xyz'
    with ctx.redirect_stdout() as out:
        yvs.main(query_str, prefs={})
        xml = out.getvalue().strip()
        root = ET.fromstring(xml)
        item = root.find('item')
        nose.assert_is_not_none(item, '<item> element is missing')
        nose.assert_equal(item.get('valid'), 'no')
