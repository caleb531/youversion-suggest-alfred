#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.view_ref as yvs
import context_managers as ctx
import inspect


def test_query_param():
    """should use received query parameter as default ref ID"""
    spec = inspect.getargspec(yvs.main)
    default_query_str = spec.defaults[0]
    nose.assert_equal(default_query_str, '{query}')


def test_url_open():
    """should attempt to open URL using webbrowser module"""
    with ctx.mock_webbrowser(yvs) as mock:
        yvs.main('59/jhn.3.17', save=False)
        nose.assert_equal(mock.url, 'https://www.bible.com/bible/59/jhn.3.17')


def test_save_recent():
    """should save reference to list of recent references"""
    with ctx.use_recent_refs([]):
        with ctx.mock_webbrowser(yvs) as mock:
            ref_uid = '59/jhn.3.17'
            yvs.main(ref_uid)
            recent_refs = yvs.shared.get_recent_refs()
            nose.assert_equal(recent_refs[0], ref_uid)
