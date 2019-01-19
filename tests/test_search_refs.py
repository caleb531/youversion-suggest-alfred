# tests.test_search_refs
# coding=utf-8

from __future__ import unicode_literals

import json

import nose.tools as nose
from mock import Mock, NonCallableMock, patch

import tests
import yvs.search_refs as yvs
from tests.decorators import redirect_stdout

with open('tests/html/search.html') as html_file:
    patch_urlopen = patch(
        'urllib2.urlopen', return_value=NonCallableMock(
            read=Mock(return_value=html_file.read())))


def set_up():
    patch_urlopen.start()
    tests.set_up()


def tear_down():
    patch_urlopen.stop()
    tests.tear_down()


@nose.with_setup(set_up, tear_down)
def test_result_titles():
    """should correctly parse result titles from HTML"""
    results = yvs.get_result_list('love others')
    nose.assert_regexp_matches(results[0]['title'], r'^Romans 13:8 \(NIV\)')
    nose.assert_regexp_matches(results[1]['title'], r'^John 15:12 \(NIV\)')
    nose.assert_regexp_matches(results[2]['title'], r'^1 Peter 4:8 \(NIV\)')
    nose.assert_equal(len(results), 3)


@nose.with_setup(set_up, tear_down)
def test_result_subtitles():
    """should correctly parse result subtitles from HTML"""
    results = yvs.get_result_list('love others')
    nose.assert_regexp_matches(results[0]['subtitle'], 'Lorem')
    nose.assert_regexp_matches(results[1]['subtitle'], 'consectetur')
    nose.assert_regexp_matches(results[2]['subtitle'], 'Ut aliquam')
    nose.assert_equal(len(results), 3)


@nose.with_setup(set_up, tear_down)
def test_result_arg():
    """should correctly parse result UID arguments from HTML"""
    results = yvs.get_result_list('love others')
    nose.assert_equal(results[0]['arg'], '111/rom.13.8')
    nose.assert_equal(results[1]['arg'], '111/jhn.15.12')
    nose.assert_equal(results[2]['arg'], '111/1pe.4.8')
    nose.assert_equal(len(results), 3)


@nose.with_setup(set_up, tear_down)
@patch('yvs.shared.get_url_content', return_value='abc')
def test_unicode_input(get_url_content):
    """should correctly handle non-ASCII characters in query string"""
    yvs.get_result_list('é')
    get_url_content.assert_called_once_with(
        'https://www.bible.com/search/bible?q=%C3%A9&version_id=111')


@nose.with_setup(set_up, tear_down)
def test_cache_url_content():
    """should cache search URL content after first fetch"""
    yvs.get_result_list('love others')
    with patch('urllib2.Request') as request:
        yvs.get_result_list('love others')
        request.assert_not_called()


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_output(out):
    """should output result list JSON"""
    query_str = 'love others'
    yvs.main(query_str)
    output = out.getvalue().strip()
    results = yvs.get_result_list(query_str)
    feedback = yvs.shared.get_result_list_feedback_str(results).strip()
    nose.assert_equal(output, feedback)


@nose.with_setup(set_up, tear_down)
@redirect_stdout
@patch('yvs.search_refs.get_result_list', return_value=[])
def test_null_result(out, get_result_list):
    """should output "No Results" JSON item for empty result list"""
    query_str = 'xyz'
    yvs.main(query_str)
    feedback_str = out.getvalue().strip()
    feedback = json.loads(feedback_str)
    nose.assert_equal(len(feedback['items']), 1, 'result item is missing')
    item = feedback['items'][0]
    nose.assert_equal(item['valid'], False)
    nose.assert_equal(item['title'], 'No Results')
