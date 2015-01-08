#!/usr/bin/env python
import unittest
import yv_suggest.search as yvs

class SearchChapterTestCase(unittest.TestCase):
    '''test the searching of Bible chapters'''

    def test_basic(self):
        '''should match chapters'''
        results = yvs.get_result_list('matthew 5')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Matthew 5')

    def test_ambiguous(self):
        '''should match chapters by ambiguous book name'''
        results = yvs.get_result_list('a 3')
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['title'], 'Amos 3')
        self.assertEqual(results[1]['title'], 'Acts 3')

    def test_whitespace(self):
        '''should match chapters irrespective of surrounding whitespace'''
        results = yvs.get_result_list('1 peter   5')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], '1 Peter 5')

    def test_id(self):
        '''should use correct ID for chapters'''
        results = yvs.get_result_list('luke 4')
        self.assertEqual(results[0]['uid'], 'niv/luk.4')

    def test_nonexistent(self):
        '''should not match nonexistent chapters'''
        results = yvs.get_result_list('psalm 160')
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
