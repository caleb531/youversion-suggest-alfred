# tests.test_set_pref
# coding=utf-8

from __future__ import unicode_literals
import json
import nose.tools as nose
import yvs.set_pref as yvs
from tests import set_up, tear_down
from tests.decorators import redirect_stdout


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_set_language(out):
    """should set preferred language"""
    yvs.main(json.dumps({
        'pref': {'id': 'language', 'name': 'Language'},
        'value': {'id': 'es', 'name': 'Español'}
    }))
    user_prefs = yvs.shared.get_user_prefs()
    nose.assert_equal(user_prefs['language'], 'es')
    bible = yvs.shared.get_bible_data(user_prefs['language'])
    nose.assert_equal(user_prefs['version'], bible['default_version'])


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_set_version(out):
    """should set preferred version"""
    yvs.main(json.dumps({
        'pref': {'id': 'version', 'name': 'Version'},
        'value': {'id': 59, 'name': 'ESV'}
    }))
    user_prefs = yvs.shared.get_user_prefs()
    nose.assert_equal(user_prefs['version'], 59)


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_set_nonexistent(out):
    """should discard nonexistent preferences"""
    yvs.main(json.dumps({
        'pref': {'id': 'foo', 'name': 'Foo'},
        'value': {'id': 'bar', 'name': 'Bar'}
    }))
    user_prefs = yvs.shared.get_user_prefs()
    nose.assert_not_in('foo', user_prefs)
