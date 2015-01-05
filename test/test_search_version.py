#!/usr/bin/env python
import unittest
import yv_suggest as yvs

class SearchVersionTestCase(unittest.TestCase):

    def test_search_version_numbered(self):
        '''should match version ending in number by partial name'''
        results = yvs.get_search_results('luke 4:8 rv1')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].subtitle, 'RV1885')

    def test_search_version_case(self):
        '''should match version irrespective of case'''
        query = 'luke 4:8 esv'
        results = yvs.get_search_results(query)
        results_lower = yvs.get_search_results(query.lower())
        results_upper = yvs.get_search_results(query.upper())
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results_lower), 1)
        self.assertEqual(len(results_upper), 1)
        self.assertDictEqual(results[0].__dict__, results_lower[0].__dict__)

    def test_search_version_partial(self):
        '''should match version by partial name'''
        results = yvs.get_search_results('luke 4:8 e')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].subtitle, 'ESV')

    def test_search_version_partial_ambig(self):
        '''should match version by ambiguous partial name'''
        results = yvs.get_search_results('luke 4:8 a')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].subtitle, 'AMP')
