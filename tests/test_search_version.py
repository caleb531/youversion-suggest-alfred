#!/usr/bin/env python
import unittest
import yv_suggest.search as yvs


class SearchVersionTestCase(unittest.TestCase):
    """test the searching of Bible references in a specific version"""

    def test_numbered(self):
        """should match versions ending in number by partial name"""
        results = yvs.get_result_list('luke 4:8 rv1')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['subtitle'], 'RV1885')

    def test_case(self):
        """should match versions irrespective of case"""
        query = 'e 4:8 esv'
        results = yvs.get_result_list(query)
        results_lower = yvs.get_result_list(query.lower())
        results_upper = yvs.get_result_list(query.upper())
        self.assertEqual(len(results), 6)
        self.assertListEqual(results_lower, results)
        self.assertListEqual(results_upper, results)

    def test_whitespace(self):
        """should match versions irrespective of surrounding whitespace"""
        results = yvs.get_result_list('1 peter 5:7    esv')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['subtitle'], 'ESV')

    def test_partial(self):
        """should match versions by partial name"""
        results = yvs.get_result_list('luke 4:8 e')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['subtitle'], 'ESV')

    def test_partial_ambiguous(self):
        """should match versions by ambiguous partial name"""
        results = yvs.get_result_list('luke 4:8 a')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['subtitle'], 'AMP')

    def test_id(self):
        """should use correct ID for versions"""
        results = yvs.get_result_list('malachi 3:2 esv')
        self.assertEqual(results[0]['uid'], 'esv/mal.3.2')

if __name__ == '__main__':
    unittest.main()
