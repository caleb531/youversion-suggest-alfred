# tests.test_set_pref

import nose.tools as nose
import yvs.set_pref as yvs


def test_set_language():
    """should set preferred language"""
    new_language = 'es'
    yvs.main('language:{}'.format(new_language))
    prefs = yvs.shared.get_prefs()
    nose.assert_equal(prefs['language'], new_language)
    bible = yvs.shared.get_bible_data(prefs['language'])
    nose.assert_equal(prefs['version'], bible['default_version'])


def test_set_version():
    """should set preferred version"""
    new_version = 59
    yvs.main('version:{}'.format(new_version))
    prefs = yvs.shared.get_prefs()
    nose.assert_equal(prefs['version'], new_version)


def test_set_search_engine():
    """should set preferred search engine"""
    new_search_engine = 'yahoo'
    yvs.main('search_engine:{}'.format(new_search_engine))
    prefs = yvs.shared.get_prefs()
    nose.assert_equal(prefs['search_engine'], new_search_engine)


def test_set_search_engine_deprecated():
    """should set preferred search engine via deprecated searchEngine key"""
    new_search_engine = 'yahoo'
    yvs.main('searchEngine:{}'.format(new_search_engine))
    prefs = yvs.shared.get_prefs()
    nose.assert_equal(prefs['search_engine'], new_search_engine)
    nose.assert_not_in('searchEngine', prefs)
