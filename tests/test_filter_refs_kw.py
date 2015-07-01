#!/usr/bin/env python

from __future__ import unicode_literals
import nose.tools as nose
import yvs.filter_refs_kw as yvs
from mock import ANY, Mock, patch
from xml.etree import ElementTree as ET
from tests.decorators import redirect_stdout, use_prefs


with open('tests/files/search.html') as file:
    patch_urlopen = patch(
        'urllib2.urlopen',
        return_value=Mock(read=Mock(return_value=file.read())))


def setup():
    patch_urlopen.start()


def teardown():
    patch_urlopen.stop()


def test_result_titles():
    '''should set result titles as full reference identifiers'''
    results = yvs.get_result_list('love others')
    nose.assert_equal(len(results), 3)
    nose.assert_equal(results[0]['title'], 'Romans 13:8 (NIV)')
    nose.assert_equal(results[1]['title'], 'John 15:12 (NIV)')
    nose.assert_equal(results[2]['title'], '1 Peter 4:8 (NIV)')


def test_result_subtitles():
    '''should set result subtitles as snippet of reference content'''
    results = yvs.get_result_list('love others')
    nose.assert_equal(len(results), 3)
    nose.assert_regexp_matches(results[0]['subtitle'], 'Lorem')
    nose.assert_regexp_matches(results[1]['subtitle'], 'consectetur')
    nose.assert_regexp_matches(results[2]['subtitle'], 'Ut aliquam')


@redirect_stdout
def test_output(out):
    """should output ref result list XML"""
    query_str = 'love others'
    yvs.main(query_str)
    output = out.getvalue().strip()
    results = yvs.get_result_list(query_str)
    xml = yvs.shared.get_result_list_xml(results).strip()
    nose.assert_equal(output, xml)


@redirect_stdout
@patch('yvs.filter_refs_kw.get_result_list', return_value=[])
def test_null_result(out, get_result_list):
    """should output "No Results" XML item for empty result list"""
    query_str = 'xyz'
    yvs.main(query_str)
    xml = out.getvalue().strip()
    root = ET.fromstring(xml)
    item = root.find('item')
    nose.assert_is_not_none(item, '<item> element is missing')
    nose.assert_equal(item.get('valid'), 'no')
    title = item.find('title')
    nose.assert_equal(title.text, 'No Results')
