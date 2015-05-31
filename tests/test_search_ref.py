#!/usr/bin/env python

import inspect
import nose.tools as nose
from mock import patch
import yv_suggest.search_ref as yvs


def test_url_open_chapter():
    """should attempt to open chapter URL using webbrowser module"""
    with patch('yv_suggest.search_ref.webbrowser'):
        yvs.main('59/jhn.3', prefs={})
        yvs.webbrowser.open.assert_called_once_with(
                          'https://www.google.com/search?q=John+3+%28ESV%29')


def test_url_open_verse():
    """should attempt to open verse URL using webbrowser module"""
    with patch('yv_suggest.search_ref.webbrowser'):
        yvs.main('59/jhn.3.17', prefs={})
        yvs.webbrowser.open.assert_called_once_with(
            'https://www.google.com/search?q=John+3%3A17+%28ESV%29')


def test_url_open_verse_range():
    """should attempt to open verse range URL using webbrowser module"""
    with patch('yv_suggest.search_ref.webbrowser'):
        yvs.main('59/jhn.3.16-17', prefs={})
        yvs.webbrowser.open.assert_called_once_with(
            'https://www.google.com/search?q=John+3%3A16-17+%28ESV%29')
