#!/usr/bin/env python3
# coding=utf-8

import json
import unittest

from nose2.tools.decorators import with_setup, with_teardown
from unittest.mock import Mock, NonCallableMock, patch

import tests
import yvs.search_refs as yvs
from tests.decorators import redirect_stdout, use_user_prefs


case = unittest.TestCase()


with open('tests/html/search.html') as html_file:
    patch_urlopen = patch(
        'urllib.request.urlopen', return_value=NonCallableMock(
            read=Mock(return_value=html_file.read())))


def set_up():
    patch_urlopen.start()
    tests.set_up()


def tear_down():
    patch_urlopen.stop()
    tests.tear_down()


@with_setup(set_up)
@with_teardown(tear_down)
def test_result_titles():
    """should correctly parse result titles from HTML"""
    results = yvs.get_result_list('love others')
    case.assertRegexpMatches(results[0]['title'], r'^Romans 13:8 \(NIV\)')
    case.assertRegexpMatches(results[1]['title'], r'^John 15:12 \(NIV\)')
    case.assertRegexpMatches(results[2]['title'], r'^1 Peter 4:8 \(NIV\)')
    case.assertEqual(len(results), 3)


@with_setup(set_up)
@with_teardown(tear_down)
def test_result_subtitles():
    """should correctly parse result subtitles from HTML"""
    results = yvs.get_result_list('love others')
    case.assertRegexpMatches(results[0]['subtitle'], 'Lorem')
    case.assertRegexpMatches(results[1]['subtitle'], 'consectetur')
    case.assertRegexpMatches(results[2]['subtitle'], 'Ut aliquam')
    case.assertEqual(len(results), 3)


@with_setup(set_up)
@with_teardown(tear_down)
def test_result_arg():
    """should correctly parse result UID arguments from HTML"""
    results = yvs.get_result_list('love others')
    case.assertEqual(results[0]['arg'], '111/rom.13.8')
    case.assertEqual(results[1]['arg'], '111/jhn.15.12')
    case.assertEqual(results[2]['arg'], '111/1pe.4.8')
    case.assertEqual(len(results), 3)


@with_setup(set_up)
@with_teardown(tear_down)
@patch('yvs.web.get_url_content', return_value='abc')
def test_unicode_input(get_url_content):
    """should correctly handle non-ASCII characters in query string"""
    yvs.get_result_list('é')
    get_url_content.assert_called_once_with(
        'https://www.bible.com/search/bible?q=%C3%A9&version_id=111')


@with_setup(set_up)
@with_teardown(tear_down)
def test_cache_url_content():
    """should cache search URL content after first fetch"""
    yvs.get_result_list('love others')
    with patch('urllib.request.Request') as request:
        yvs.get_result_list('love others')
        request.assert_not_called()


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs({'language': 'eng', 'version': 111, 'copybydefault': False})
def test_copy_by_default_false():
    """should export correct data when "Copy By Default?" setting is false"""
    results = yvs.get_result_list('love others')
    case.assertEqual(results[0]['variables']['copybydefault'], 'False')
    case.assertEqual(
        results[0]['subtitle'], '» “Lorem ipsum” dolor sit amet,')
    case.assertEqual(
        results[0]['mods']['cmd']['subtitle'], 'Copy content to clipboard')


@with_setup(set_up)
@with_teardown(tear_down)
@use_user_prefs({'language': 'eng', 'version': 111, 'copybydefault': True})
def test_copy_by_default_true():
    """should export correct data when "Copy By Default?" setting is true"""
    results = yvs.get_result_list('love others')
    case.assertEqual(results[0]['variables']['copybydefault'], 'True')
    case.assertEqual(
        results[0]['subtitle'], '» “Lorem ipsum” dolor sit amet,')
    case.assertEqual(
        results[0]['mods']['cmd']['subtitle'], 'View on YouVersion')


@with_setup(set_up)
@with_teardown(tear_down)
def test_structure():
    """JSON should match result list"""
    results = yvs.get_result_list('love others')
    result = results[0]
    feedback_str = yvs.core.get_result_list_feedback_str(results)
    feedback = json.loads(feedback_str)
    case.assertIn('items', feedback, 'feedback object must have result items')
    item = feedback['items'][0]
    case.assertNotIn('uid', item)
    case.assertEqual(item['arg'], result['arg'])
    case.assertEqual(
        item['quicklookurl'], 'https://www.bible.com/bible/111/ROM.13.8')
    case.assertEqual(item['title'], 'Romans 13:8 (NIV) ♥')
    case.assertEqual(item['text']['copy'], result['title'])
    case.assertEqual(item['text']['largetype'], result['title'])
    case.assertEqual(item['subtitle'], result['subtitle'])
    case.assertEqual(item['icon']['path'], 'icon.png')


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
def test_output(out):
    """should output result list JSON"""
    query_str = 'love others'
    yvs.main(query_str)
    output = out.getvalue().rstrip()
    results = yvs.get_result_list(query_str)
    feedback = yvs.core.get_result_list_feedback_str(results).rstrip()
    case.assertEqual(output, feedback)


@with_setup(set_up)
@with_teardown(tear_down)
@redirect_stdout
@patch('yvs.search_refs.get_result_list', return_value=[])
def test_null_result(out, get_result_list):
    """should output "No Results" JSON item for empty result list"""
    query_str = 'xyz'
    yvs.main(query_str)
    feedback_str = out.getvalue()
    feedback = json.loads(feedback_str)
    case.assertEqual(len(feedback['items']), 1, 'result item is missing')
    item = feedback['items'][0]
    case.assertEqual(item['valid'], False)
    case.assertEqual(item['title'], 'No Results')
