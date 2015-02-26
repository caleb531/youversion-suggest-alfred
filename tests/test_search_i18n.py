#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import nose.tools as nose
import yv_suggest.search as yvs


def test_spanish():
    """should match Spanish Bible references"""
    yvs.shared.preferred_language = 'es'
    results = yvs.get_result_list('gá 2')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], 'Gálatas 2 (NVI)')
    yvs.shared.preferred_language = 'en'
