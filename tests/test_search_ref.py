#!/usr/bin/env python

import nose.tools as nose
import yv_suggest.search_ref as yvs
import context_managers as ctx
import inspect


def test_url_open_chapter():
    """should attempt to open chapter URL using webbrowser module"""
    with ctx.mock_webbrowser(yvs) as mock:
        yvs.main('59/jhn.3', prefs={})
        nose.assert_equal(mock.url,
                          'https://www.google.com/search?q=John+3+%28ESV%29')


def test_url_open_verse():
    """should attempt to open verse URL using webbrowser module"""
    with ctx.mock_webbrowser(yvs) as mock:
        yvs.main('59/jhn.3.17', prefs={})
        url = 'https://www.google.com/search?q=John+3%3A17+%28ESV%29'
        nose.assert_equal(mock.url, url)


def test_url_open_verse_range():
    """should attempt to open verse range URL using webbrowser module"""
    with ctx.mock_webbrowser(yvs) as mock:
        yvs.main('59/jhn.3.16-17', prefs={})
        url = 'https://www.google.com/search?q=John+3%3A16-17+%28ESV%29'
        nose.assert_equal(mock.url, url)
