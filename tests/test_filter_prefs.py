# tests.test_filter_prefs

from __future__ import unicode_literals
import nose.tools as nose
import yvs.filter_prefs as yvs
from xml.etree import ElementTree as ETree
from tests.decorators import redirect_stdout, use_user_prefs


def test_show_languages():
    """should show all languages if no value is given"""
    results = yvs.get_result_list('language')
    nose.assert_equal(len(results), 21)


def test_filter_languages():
    """should filter available languages if value is given"""
    results = yvs.get_result_list('language p')
    nose.assert_equal(len(results), 3)
    nose.assert_equal(results[0]['title'], 'Polski')
    nose.assert_equal(results[0]['arg'], 'language:pl')


@use_user_prefs({'language': 'es', 'version': 128})
def test_show_versions():
    """should show all versions if no value is given"""
    results = yvs.get_result_list('version')
    nose.assert_equal(len(results), 13)


def test_filter_versions():
    """should filter available versions if value is given"""
    results = yvs.get_result_list('version ni')
    nose.assert_equal(len(results), 3)
    nose.assert_equal(results[0]['title'], 'NIRV')
    nose.assert_equal(results[0]['arg'], 'version:110')


def test_show_search_enginges():
    """should show all search engines if no value is given"""
    results = yvs.get_result_list('searchEngine')
    nose.assert_equal(len(results), 4)


def test_filter_search_engines():
    """should filter available search engines if value is given"""
    results = yvs.get_result_list('searchEngine y')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Yahoo!')
    nose.assert_equal(results[0]['arg'], 'searchEngine:yahoo')


def test_nonexistent_pref():
    """should not match nonexistent preference"""
    results = yvs.get_result_list('xyz')
    nose.assert_equal(len(results), 0)


def test_nonexistent_value():
    """should return null result for nonexistent value"""
    results = yvs.get_result_list('language xyz')
    nose.assert_equal(len(results), 1)
    nose.assert_regexp_matches(results[0]['title'], 'No Results')
    nose.assert_equal(results[0]['valid'], 'no')


def test_current_value():
    """should not make preference's current value actionable"""
    results = yvs.get_result_list('language english')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'English')
    nose.assert_equal(results[0]['valid'], 'no')


def test_invalid_query():
    """should show all available preferences for invalid preference name"""
    results = yvs.get_result_list('!@#')
    nose.assert_not_equal(len(results), 0)


def test_nonexistent_preference():
    """should show null result if preference matching query does not exist"""
    results = yvs.get_result_list('xyz')
    nose.assert_equal(len(results), 0)


def test_non_alphanumeric():
    """should ignore all non-alphanumeric characters"""
    results = yvs.get_result_list('!language@it#')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Italiano')


def test_show_all_preferences():
    """should show all available preferences if query is empty"""
    results = yvs.get_result_list('')
    nose.assert_not_equal(len(results), 0)


def test_preferences_autocompletion():
    """autocompletion should be functioning for all preference results"""
    results = yvs.get_result_list('')
    for result in results:
        nose.assert_in('autocomplete', result)
        nose.assert_in('valid', result)
        nose.assert_equal(result['valid'], 'no')


def test_filter_preferences():
    """should filter available preferences if partial key name is given"""
    results = yvs.get_result_list('searche')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Search Engine')


@redirect_stdout
def test_main_output(out):
    """should output pref result list XML"""
    query_str = 'language'
    yvs.main(query_str)
    output = out.getvalue().strip()
    results = yvs.get_result_list(query_str)
    xml = yvs.shared.get_result_list_xml(results).strip()
    nose.assert_equal(output, xml)


@redirect_stdout
def test_null_result(out):
    """should output "No Results" XML item for empty pref result list"""
    query_str = 'xyz'
    yvs.main(query_str)
    xml = out.getvalue().strip()
    root = ETree.fromstring(xml)
    item = root.find('item')
    nose.assert_is_not_none(item, '<item> element is missing')
    nose.assert_equal(item.get('valid'), 'no')


@redirect_stdout
def test_xml_show_all(out):
    """should output XML for all results if query is empty"""
    yvs.main('')
    output = out.getvalue().strip()
    results = yvs.get_result_list('')
    xml = yvs.shared.get_result_list_xml(results).strip()
    nose.assert_equal(output, xml)
