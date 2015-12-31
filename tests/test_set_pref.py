# tests.test_set_pref

import nose.tools as nose
import yvs.set_pref as yvs


def test_set_language():
    """should set preferred language"""
    new_language = 'es'
    yvs.main('language:{}'.format(new_language))
    user_prefs = yvs.shared.get_user_prefs()
    nose.assert_equal(user_prefs['language'], new_language)
    bible = yvs.shared.get_bible_data(user_prefs['language'])
    nose.assert_equal(user_prefs['version'], bible['default_version'])


def test_set_version():
    """should set preferred version"""
    new_version = 59
    yvs.main('version:{}'.format(new_version))
    user_prefs = yvs.shared.get_user_prefs()
    nose.assert_equal(user_prefs['version'], new_version)


def test_set_search_engine():
    """should set preferred search engine"""
    new_search_engine = 'yahoo'
    yvs.main('searchEngine:{}'.format(new_search_engine))
    user_prefs = yvs.shared.get_user_prefs()
    nose.assert_equal(user_prefs['searchEngine'], new_search_engine)
