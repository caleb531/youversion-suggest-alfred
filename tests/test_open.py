#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.open as yvo
from webbrowser_mock import WebbrowserMock
import inspect


def test_query_param():
    """should use received query parameter as default ref ID"""
    spec = inspect.getargspec(yvo.main)
    default_query_str = spec.defaults[0]
    nose.assert_equal(default_query_str, '{query}')


def test_url_open():
    """should attempt to open URL using webbrowser module"""
    mock = WebbrowserMock()
    yvo.webbrowser = mock
    yvo.main('59/jhn.3.17')
    nose.assert_equal(mock.url, 'https://www.bible.com/bible/59/jhn.3.17')
