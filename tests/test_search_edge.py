#!/usr/bin/env python

import nose.tools as nose
import yv_suggest.search as yvs


def test_littered():
    """should match reference literred with non-alphanumeric characters"""
    results = yvs.get_result_list('1 co@13#4$7^e')
    nose.assert_equal(len(results), 1)
    nose.assert_equal(results[0]['title'], '1 Corinthians 13:4-7 (ESV)')
