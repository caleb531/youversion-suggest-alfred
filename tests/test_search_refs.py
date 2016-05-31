# tests.test_search_refs
# coding=utf-8

from __future__ import unicode_literals
import hashlib
import json
import os
import os.path
import nose.tools as nose
import tests
import yvs.search_refs as yvs
from mock import Mock, NonCallableMock, patch
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
    nose.assert_equal(len(results), 3)
    nose.assert_regexp_matches(results[0]['title'], r'^Romans 13:8 \(NIV\)')
    nose.assert_regexp_matches(results[1]['title'], r'^John 15:12 \(NIV\)')
    nose.assert_regexp_matches(results[2]['title'], r'^1 Peter 4:8 \(NIV\)')


@nose.with_setup(set_up, tear_down)
def test_result_subtitles():
    """should correctly parse result subtitles from HTML"""
    results = yvs.get_result_list('love others')
    nose.assert_equal(len(results), 3)
    nose.assert_regexp_matches(results[0]['subtitle'], 'Lorem')
    nose.assert_regexp_matches(results[1]['subtitle'], 'consectetur')
    nose.assert_regexp_matches(results[2]['subtitle'], 'Ut aliquam')


@nose.with_setup(set_up, tear_down)
def test_result_arg():
    """should correctly parse result UID arguments from HTML"""
    results = yvs.get_result_list('love others')
    nose.assert_equal(len(results), 3)
    nose.assert_equal(results[0]['arg'], '111/rom.13.8')
    nose.assert_equal(results[1]['arg'], '111/jhn.15.12')
    nose.assert_equal(results[2]['arg'], '111/1pe.4.8')


@nose.with_setup(set_up, tear_down)
@patch('urllib2.Request')
def test_unicode_input(request):
    """should correctly handle non-ASCII characters in query string"""
    results = yvs.get_result_list('é')
    request.assert_called_once_with(
        'https://www.bible.com/search/bible?q=%C3%A9&version_id=111',
        headers={'User-Agent': 'YouVersion Suggest'})
    nose.assert_equal(len(results), 3)


@nose.with_setup(set_up, tear_down)
def test_charref_dec_title():
    """should evaluate character references in result titles"""
    results = yvs.get_result_list('love others')
    nose.assert_equal(len(results), 3)
    nose.assert_equal(results[0]['title'], 'Romans 13:8 (NIV) \u2665')


@nose.with_setup(set_up, tear_down)
def test_charref_dec_subtitle():
    """should evaluate character references in result subtitles"""
    results = yvs.get_result_list('love others')
    nose.assert_equal(len(results), 3)
    nose.assert_regexp_matches(
        results[0]['subtitle'], '\u201cLorem ipsum\u201d')


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
    nose.assert_equal(item['valid'], 'no')
    nose.assert_equal(item['title'], 'No Results')


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_cache_feedback_results(out):
    """should cache final JSON results after first fetch and parse"""
    query_str = 'love others'
    yvs.main(query_str)
    fetched_content = out.getvalue()
    out.seek(0)
    out.truncate(0)
    with patch('urllib2.Request') as request:
        yvs.main(query_str)
        cached_content = out.getvalue()
        nose.assert_equal(cached_content, fetched_content)
        request.assert_not_called()


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_cache_housekeeping(out):
    """should purge oldest entry when cache grows too large"""
    query_str = 'a'
    num_entries = 101
    purged_entry_checksum = hashlib.sha1('yvsearch {}.json'.format(
        'a' * 1).encode('utf-8')).hexdigest()
    last_entry_checksum = hashlib.sha1('yvsearch {}.json'.format(
        'a' * num_entries).encode('utf-8')).hexdigest()
    nose.assert_false(
        os.path.exists(yvs.shared.get_cache_entry_dir_path()),
        'local cache entry directory exists')
    for i in range(num_entries):
        yvs.main(query_str)
        query_str += 'a'
    entry_checksums = os.listdir(yvs.shared.get_cache_entry_dir_path())
    nose.assert_equal(len(entry_checksums), 100)
    nose.assert_not_in(purged_entry_checksum, entry_checksums)
    nose.assert_in(last_entry_checksum, entry_checksums)
