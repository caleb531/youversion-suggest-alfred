#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.filter_recent_refs as yvs
import context_managers as ctx
import inspect
from xml.etree import ElementTree as ET


recent_refs = ['59/psa.23', '116/1co.13', '107/psa.139', '111/psa.22',
               '59/rev.5.13', '1/psa.23', '111/mat.5.3-12',
               '8/rev.19.16', '111/rev.22', '8/psa.23']


def test_query_param():
    """should use received query parameter as default filter query"""
    spec = inspect.getargspec(yvs.main)
    default_query_str = spec.defaults[0]
    nose.assert_equal(default_query_str, '{query}')


def test_show_all():
    """should show all recent references when given empty query"""
    with ctx.use_recent_refs(recent_refs):
        results = yvs.get_result_list('', prefs={})
        nose.assert_equal(len(results), len(recent_refs))


def test_filter_book():
    """should filter recent references by book name"""
    with ctx.use_recent_refs(recent_refs):
        results = yvs.get_result_list('ps', prefs={})
        nose.assert_equal(len(results), 5)
        nose.assert_equal(results[0]['title'], 'Psalm 23 (ESV)')
        nose.assert_equal(results[1]['title'], 'Psalm 139 (NET)')
        nose.assert_equal(results[2]['title'], 'Psalm 22 (NIV)')
        nose.assert_equal(results[3]['title'], 'Psalm 23 (KJV)')
        nose.assert_equal(results[4]['title'], 'Psalm 23 (AMP)')


def test_filter_book_numbered():
    """should filter recent references by numbered book name"""
    with ctx.use_recent_refs(recent_refs):
        results = yvs.get_result_list('1c', prefs={})
        nose.assert_equal(len(results), 1)
        nose.assert_equal(results[0]['title'], '1 Corinthians 13 (NLT)')


def test_filter_chapter():
    """should filter recent references by chapter"""
    with ctx.use_recent_refs(recent_refs):
        results = yvs.get_result_list('re1', prefs={})
        nose.assert_equal(len(results), 1)
        nose.assert_equal(results[0]['title'], 'Revelation 19:16 (AMP)')


def test_filter_verse():
    """should filter recent references by verse"""
    with ctx.use_recent_refs(recent_refs):
        results = yvs.get_result_list('re5.1', prefs={})
        nose.assert_equal(len(results), 1)
        nose.assert_equal(results[0]['title'], 'Revelation 5:13 (ESV)')


def test_filter_verse_range():
    """should filter recent references by verse range"""
    with ctx.use_recent_refs(recent_refs):
        results = yvs.get_result_list('m5:3-1', prefs={})
        nose.assert_equal(len(results), 1)
        nose.assert_equal(results[0]['title'], 'Matthew 5:3-12 (NIV)')


def test_filter_version():
    """should filter recent references by version"""
    with ctx.use_recent_refs(recent_refs):
        results = yvs.get_result_list('ps2k', prefs={})
        nose.assert_equal(len(results), 1)
        nose.assert_equal(results[0]['title'], 'Psalm 23 (KJV)')


def test_filter_empty():
    """should return empty list for nonexistent references"""
    with ctx.use_recent_refs(recent_refs):
        results = yvs.get_result_list('xyz', prefs={})
        nose.assert_equal(len(results), 0)


def test_main_output():
    """should output recent list XML"""
    with ctx.use_recent_refs(recent_refs):
        with ctx.redirect_stdout() as out:
            query_str = 'p22'
            yvs.main(query_str, prefs={})
            output = out.getvalue().strip()
            results = yvs.get_result_list(query_str, prefs={})
            xml = yvs.shared.get_result_list_xml(results).strip()
            nose.assert_equal(output, xml)


def test_null_result():
    """should output "No Results" XML item for empty recent recent list"""
    with ctx.use_recent_refs(recent_refs):
        with ctx.redirect_stdout() as out:
            yvs.main('xyz', prefs={})
            xml = out.getvalue().strip()
            root = ET.fromstring(xml)
            item = root.find('item')
            nose.assert_is_not_none(item, '<item> element is missing')
            nose.assert_equal(item.get('valid'), 'no')
