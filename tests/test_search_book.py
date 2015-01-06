#!/usr/bin/env python
import unittest
import yv_suggest as yvs

class SearchBookTestCase(unittest.TestCase):
    '''test the searching of Bible books'''

    def test_search_book_partial(self):
        '''should match books by partial name'''
        results = yvs.get_result_list('luk')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Luke')

    def test_search_book_case(self):
        '''should match books irrespective of case'''
        query = 'Matthew'
        results = yvs.get_result_list(query)
        results_lower = yvs.get_result_list(query.lower())
        results_upper = yvs.get_result_list(query.upper())
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results_lower), 1)
        self.assertEqual(len(results_upper), 1)
        self.assertDictEqual(results[0].__dict__, results_lower[0].__dict__)

    def test_search_book_partial_ambig(self):
        '''should match books by ambiguous partial name'''
        results = yvs.get_result_list('r')
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].title, 'Ruth')
        self.assertEqual(results[1].title, 'Romans')
        self.assertEqual(results[2].title, 'Revelation')

    def test_search_book_multiple_words(self):
        '''should match books with names comprised of multiple words'''
        results = yvs.get_result_list('song of songs')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Song of Songs')

    def test_search_book_numbered_partial(self):
        '''should match numbered books by partial numbered name'''
        results = yvs.get_result_list('1 cor')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, '1 Corinthians')

    def test_search_book_nonnumbered_partial(self):
        '''should match numbered books by partial non-numbered name'''
        results = yvs.get_result_list('john')
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0].title, 'John')
        self.assertEqual(results[1].title, '1 John')
        self.assertEqual(results[2].title, '2 John')
        self.assertEqual(results[3].title, '3 John')

    def test_search_book_id(self):
        '''should use correct ID for books'''
        results = yvs.get_result_list('philippians')
        self.assertEqual(results[0].uid, 'niv/php.1')

    def test_search_book_nonexistent(self):
        '''should not match nonexistent books'''
        results = yvs.get_result_list('jesus')
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
