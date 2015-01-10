#!/usr/bin/env python
import unittest
import yv_suggest.open as yvs
import inspect

class OpenReferenceTest(unittest.TestCase):
    '''test the handling of Bible reference URLs'''

    def test_url(self):
        '''should build correct URL to Bible reference'''
        url = yvs.get_ref_url('esv/jhn.3.16')
        self.assertEqual(url, 'https://www.bible.com/bible/esv/jhn.3.16')

    def test_query_param(self):
        '''should receive chosen item's arg as the default ref ID'''
        spec = inspect.getargspec(yvs.main)
        default_query_str = spec.defaults[0]
        self.assertEqual(default_query_str, '{query}')
