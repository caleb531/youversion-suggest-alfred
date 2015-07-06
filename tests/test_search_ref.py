# tests.test_search_ref

import nose.tools as nose
import yvs.search_ref as yvs
from mock import patch
from tests.decorators import use_prefs


@patch('webbrowser.open')
def test_url_open_chapter(open):
    """should open chapter search URL"""
    yvs.main('59/jhn.3')
    open.assert_called_once_with(
        'https://www.google.com/search?q=John+3+%28ESV%29')


@patch('webbrowser.open')
def test_url_open_verse(open):
    """should open verse search URL"""
    yvs.main('59/jhn.3.17')
    open.assert_called_once_with(
        'https://www.google.com/search?q=John+3%3A17+%28ESV%29')


@patch('webbrowser.open')
def test_url_open_verse_range(open):
    """should open verse range search URL"""
    yvs.main('59/jhn.3.16-17')
    open.assert_called_once_with(
        'https://www.google.com/search?q=John+3%3A16-17+%28ESV%29')


@use_prefs({'language': 'es'})
@patch('webbrowser.open')
def test_unicode_search(open):
    """should open search URL for reference containing Unicode"""
    yvs.main('128/exo.4')
    open.assert_called_once_with(
        'https://www.google.com/search?q=%C3%89xodo+4+%28NVI%29')
