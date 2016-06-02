# tests.test_filter_prefs
# coding=utf-8

from __future__ import unicode_literals
import json
import nose.tools as nose
import yvs.filter_prefs as yvs
from tests import set_up, tear_down
from tests.decorators import redirect_stdout, use_user_prefs


@nose.with_setup(set_up, tear_down)
def test_show_languages():
    """should show all languages if no value is given"""
    results = yvs.get_result_list('language')
    nose.assert_equal(len(results), 21)


@nose.with_setup(set_up, tear_down)
def test_filter_languages():
    """should filter available languages if value is given"""
    results = yvs.get_result_list('language español')
    nose.assert_equal(len(results), 2)
    nose.assert_equal(results[0]['uid'], 'yvs-language-es')
    nose.assert_equal(results[0]['title'], 'Español')
    nose.assert_equal(results[0]['arg'], 'language:es')


@nose.with_setup(set_up, tear_down)
@use_user_prefs({'language': 'es', 'version': 128})
def test_show_versions():
    """should show all versions if no value is given"""
    results = yvs.get_result_list('version')
    nose.assert_equal(len(results), 13)


@nose.with_setup(set_up, tear_down)
def test_filter_versions():
    """should filter available versions if value is given"""
    results = yvs.get_result_list('version ni')
    nose.assert_equal(len(results), 3)
    nose.assert_equal(results[0]['uid'], 'yvs-version-110')
    nose.assert_equal(results[0]['title'], 'NIRV')
    nose.assert_equal(results[0]['arg'], 'version:110')


@nose.with_setup(set_up, tear_down)
def test_show_search_engines():
    """should show all search engines if no value is given"""
    results = yvs.get_result_list('search_engine')
    nose.assert_equal(len(results), 4)


@nose.with_setup(set_up, tear_down)
def test_filter_search_engines():
    """should filter available search engines if value is given"""
    results = yvs.get_result_list('search_engine y')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['uid'], 'yvs-search_engine-yahoo')
    nose.assert_equal(results[0]['title'], 'Yahoo!')
    nose.assert_equal(results[0]['arg'], 'search_engine:yahoo')


@nose.with_setup(set_up, tear_down)
def test_nonexistent_pref():
    """should not match nonexistent preference"""
    results = yvs.get_result_list('xyz')
    nose.assert_equal(len(results), 0)


@nose.with_setup(set_up, tear_down)
def test_nonexistent_value():
    """should return null result for nonexistent value"""
    results = yvs.get_result_list('language xyz')
    nose.assert_equal(len(results), 1)
    nose.assert_regexp_matches(results[0]['title'], 'No Results')
    nose.assert_equal(results[0]['valid'], 'no')


@nose.with_setup(set_up, tear_down)
def test_current_value():
    """should not make preference's current value actionable"""
    results = yvs.get_result_list('language english')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'English')
    nose.assert_equal(results[0]['valid'], 'no')


@nose.with_setup(set_up, tear_down)
def test_invalid_query():
    """should show all available preferences for invalid preference name"""
    results = yvs.get_result_list('!@#')
    nose.assert_not_equal(len(results), 0)


@nose.with_setup(set_up, tear_down)
def test_nonexistent_preference():
    """should show null result if preference matching query does not exist"""
    results = yvs.get_result_list('xyz')
    nose.assert_equal(len(results), 0)


@nose.with_setup(set_up, tear_down)
def test_non_alphanumeric():
    """should ignore all non-alphanumeric characters"""
    results = yvs.get_result_list('!language@it#')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Italiano')


@nose.with_setup(set_up, tear_down)
def test_show_all_preferences():
    """should show all available preferences if query is empty"""
    results = yvs.get_result_list('')
    nose.assert_not_equal(len(results), 0)


@nose.with_setup(set_up, tear_down)
def test_preferences_autocompletion():
    """autocompletion should be functioning for all preference results"""
    results = yvs.get_result_list('')
    for result in results:
        nose.assert_in('autocomplete', result)
        nose.assert_in('valid', result)
        nose.assert_equal(result['valid'], 'no')


@nose.with_setup(set_up, tear_down)
def test_filter_preferences():
    """should filter available preferences if partial key name is given"""
    results = yvs.get_result_list('searche')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['uid'], 'yvs-search_engine')
    nose.assert_equal(results[0]['title'], 'Search Engine')


@nose.with_setup(set_up, tear_down)
def test_filter_preferences_show_current():
    """should show current values for all preferences"""
    results = yvs.get_result_list('')
    nose.assert_in('English', results[0]['subtitle'])
    nose.assert_in('NIV', results[1]['subtitle'])
    nose.assert_in('Google', results[2]['subtitle'])


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_main_output(out):
    """should output pref result list JSON"""
    query_str = 'language'
    yvs.main(query_str)
    output = out.getvalue().strip()
    results = yvs.get_result_list(query_str)
    feedback = yvs.shared.get_result_list_feedback_str(results).strip()
    nose.assert_equal(output, feedback)


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_null_result(out):
    """should output "No Results" JSON item for empty pref result list"""
    query_str = 'xyz'
    yvs.main(query_str)
    feedback_str = out.getvalue().strip()
    feedback = json.loads(feedback_str)
    nose.assert_equal(len(feedback['items']), 1, 'result item is missing')
    item = feedback['items'][0]
    nose.assert_equal(item['title'], 'No Results')
    nose.assert_equal(item['valid'], 'no')


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_feedback_show_all(out):
    """should output JSON for all results if query is empty"""
    yvs.main('')
    output = out.getvalue().strip()
    results = yvs.get_result_list('')
    feedback = yvs.shared.get_result_list_feedback_str(results).strip()
    nose.assert_equal(output, feedback)
