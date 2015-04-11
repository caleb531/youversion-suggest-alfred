#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.view_ref as yvs
import context_managers as ctx
import inspect


def test_url_open():
    """should attempt to open URL using webbrowser module"""
    with ctx.mock_webbrowser(yvs) as mock:
        yvs.main('59/jhn.3.17')
        nose.assert_equal(mock.url, 'https://www.bible.com/bible/59/jhn.3.17')
