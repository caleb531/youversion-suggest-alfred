# tests.test_set_pref

import nose.tools as nose
import yvs.set_pref as yvs
from tests import set_up, tear_down


@nose.with_setup(set_up, tear_down)
def test_set_language():
    """should set preferred language"""
    new_language = 'es'
    yvs.main('language:{}'.format(new_language))
    user_prefs = yvs.shared.get_user_prefs()
    nose.assert_equal(user_prefs['language'], new_language)
    bible = yvs.shared.get_bible_data(user_prefs['language'])
    nose.assert_equal(user_prefs['version'], bible['default_version'])


@nose.with_setup(set_up, tear_down)
def test_set_version():
    """should set preferred version"""
    new_version = 59
    yvs.main('version:{}'.format(new_version))
    user_prefs = yvs.shared.get_user_prefs()
    nose.assert_equal(user_prefs['version'], new_version)


@nose.with_setup(set_up, tear_down)
def test_set_search_engine():
    """should set preferred search engine"""
    new_search_engine = 'yahoo'
    yvs.main('searchEngine:{}'.format(new_search_engine))
    user_prefs = yvs.shared.get_user_prefs()
    nose.assert_equal(user_prefs['searchEngine'], new_search_engine)


@nose.with_setup(set_up, tear_down)
def test_set_nonstandard():
    """should discard non-standard preferences"""
    yvs.main('foo:bar')
    user_prefs = yvs.shared.get_user_prefs()
    nose.assert_not_in('foo', user_prefs)
