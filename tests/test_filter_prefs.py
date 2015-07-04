# tests.test_filter_prefs

from __future__ import unicode_literals
import nose.tools as nose
import yvs.filter_prefs as yvs
from xml.etree import ElementTree as ET
from tests.decorators import redirect_stdout


def test_show_languages():
    """should show all languages if no value is given"""
    results = yvs.get_result_list('language')
    nose.assert_not_equal(len(results), 0)


def test_filter_languages():
    """should filter available languages if value is given"""
    results = yvs.get_result_list('language en')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'English')
    nose.assert_equal(results[0]['arg'], 'language:en')


def test_show_versions():
    """should show all versions if no value is given"""
    results = yvs.get_result_list('version')
    nose.assert_not_equal(len(results), 0)


def test_filter_versions():
    """should filter available versions if value is given"""
    results = yvs.get_result_list('version ni')
    nose.assert_equal(len(results), 3)
    nose.assert_equal(results[0]['title'], 'NIRV')
    nose.assert_equal(results[0]['arg'], 'version:110')


def test_nonexistent():
    """should not match nonexistent preference"""
    results = yvs.get_result_list('xyz')
    nose.assert_equal(len(results), 0)


def test_invalid():
    """should show all existing preferences for invalid preference name"""
    results = yvs.get_result_list('!@#')
    nose.assert_equal(len(results), 2)
    nose.assert_equal(results[0]['title'], 'Language')
    nose.assert_equal(results[1]['title'], 'Version')


def test_empty():
    """should show all existing preferences if query is empty"""
    results = yvs.get_result_list('')
    nose.assert_equal(len(results), 2)
    nose.assert_equal(results[0]['title'], 'Language')
    nose.assert_equal(results[1]['title'], 'Version')


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
    root = ET.fromstring(xml)
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
