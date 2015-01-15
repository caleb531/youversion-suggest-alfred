#!/usr/bin/env python
import unittest
import yv_suggest.search as yvs

class SearchIncompleteTestCase(unittest.TestCase):
    '''test the searching of incomplete Bible references'''

    def test_incomplete_verse(self):
        '''should treat incomplete verse reference as chapter reference'''
        results = yvs.get_result_list('psalm 19:')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Psalm 19')

    def test_incomplete_dot_verse(self):
        '''should treat incomplete "dot verse" reference as chapter reference'''
        results = yvs.get_result_list('psalm 19.')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Psalm 19')

    def test_incomplete_verse_range(self):
        '''should treat incomplete verse ranges as single-verse references'''
        results = yvs.get_result_list('psalm 19.7-')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Psalm 19.7')

if __name__ == '__main__':
    unittest.main()
