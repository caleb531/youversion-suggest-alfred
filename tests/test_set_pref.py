#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.set_pref as yvs
import context_managers as ctx


def test_set_language():
    """should set preferred language"""
    with ctx.get_prefs() as prefs:
        languages = yvs.shared.get_languages()
        for language in languages:
            if language['id'] != prefs['language']:
                new_language = language['id']
                break
        yvs.main('language:{}'.format(new_language))
        # Check if new values have been saved to preferences
        prefs = yvs.shared.get_prefs()
        bible = yvs.shared.get_bible_data(prefs['language'])
        nose.assert_equal(prefs['language'], new_language)
        nose.assert_equal(prefs['version'], bible['default_version'])


def test_set_version():
    """should set preferred version"""
    with ctx.get_prefs() as prefs:
        bible = yvs.shared.get_bible_data(prefs['language'])
        versions = bible['versions']
        for version in versions:
            if version['id'] != prefs['language']:
                new_version = version['id']
                break
        yvs.main('version:{}'.format(new_version))
        # Check if new values have been saved to preferences
        prefs = yvs.shared.get_prefs()
        nose.assert_equal(prefs['version'], new_version)
