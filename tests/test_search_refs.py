# tests.test_search_refs
# coding=utf-8

from __future__ import unicode_literals
import nose.tools as nose
import yvs.search_refs as yvs
from mock import Mock, NonCallableMock, patch
from xml.etree import ElementTree as ETree
from tests.decorators import redirect_stdout


with open('tests/files/search.html') as html_file:
    patch_urlopen = patch(
        'urllib2.urlopen', return_value=NonCallableMock(
            read=Mock(return_value=html_file.read())))


def setup():
    patch_urlopen.start()


def teardown():
    patch_urlopen.stop()


def test_result_titles():
    '''should set result titles as full reference identifiers'''
    results = yvs.get_result_list('love others')
    nose.assert_equal(len(results), 3)
    nose.assert_regexp_matches(results[0]['title'], r'Romans 13:8 \(NIV\)')
    nose.assert_regexp_matches(results[1]['title'], r'John 15:12 \(NIV\)')
    nose.assert_regexp_matches(results[2]['title'], r'1 Peter 4:8 \(NIV\)')


def test_result_subtitles():
    '''should set result subtitles as snippet of reference content'''
    results = yvs.get_result_list('love others')
    nose.assert_equal(len(results), 3)
    nose.assert_regexp_matches(results[0]['subtitle'], 'Lorem')
    nose.assert_regexp_matches(results[1]['subtitle'], 'consectetur')
    nose.assert_regexp_matches(results[2]['subtitle'], 'Ut aliquam')


@patch('urllib2.Request')
def test_unicode_input(request):
    '''should not raise exception when input contains non-ASCII characters'''
    results = yvs.get_result_list('é')
    request.assert_called_once_with(
        'https://www.bible.com/search/bible?q=%C3%A9&version_id=111',
        headers={'User-Agent': 'YouVersion Suggest'})
    nose.assert_equal(len(results), 3)


def test_charref_dec_title():
    '''should evaluate character references in result titles'''
    results = yvs.get_result_list('love others')
    nose.assert_equal(len(results), 3)
    nose.assert_regexp_matches(
        results[0]['title'], r'Romans 13:8 \(NIV\) \u2665')


def test_charref_dec_subtitle():
    '''should evaluate character references in result subtitles'''
    results = yvs.get_result_list('love others')
    nose.assert_equal(len(results), 3)
    nose.assert_regexp_matches(
        results[0]['subtitle'], '\u201cLorem ipsum\u201d')


@redirect_stdout
def test_output(out):
    """should output result list XML"""
    query_str = 'love others'
    yvs.main(query_str)
    output = out.getvalue().strip()
    results = yvs.get_result_list(query_str)
    xml = yvs.shared.get_result_list_xml(results).strip()
    nose.assert_equal(output, xml)


@redirect_stdout
@patch('yvs.search_refs.get_result_list', return_value=[])
def test_null_result(out, get_result_list):
    """should output "No Results" XML item for empty result list"""
    query_str = 'xyz'
    yvs.main(query_str)
    xml = out.getvalue().strip()
    root = ETree.fromstring(xml)
    item = root.find('item')
    nose.assert_is_not_none(item, '<item> element is missing')
    nose.assert_equal(item.get('valid'), 'no')
    title = item.find('title')
    nose.assert_equal(title.text, 'No Results')
