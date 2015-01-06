#!/usr/bin/env python
import unittest
import yv_suggest as yvs

class OpenReferenceTest(unittest.TestCase):
    '''test the handling of Bible reference URLs'''

    def test_get_ref_url(self):
        '''should build correct URL to Bible reference'''
        url = yvs.get_ref_url('esv/jhn.3.16')
        self.assertEqual(url, 'https://www.bible.com/bible/esv/jhn.3.16')
