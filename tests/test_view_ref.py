#!/usr/bin/env python

import inspect
import nose.tools as nose
from mock import patch
import yv_suggest.view_ref as yvs


def test_url_open():
    """should attempt to open URL using webbrowser module"""
    with patch('yv_suggest.view_ref.webbrowser'):
        yvs.main('59/jhn.3.17')
        yvs.webbrowser.open.assert_called_once_with(
            'https://www.bible.com/bible/59/jhn.3.17')
