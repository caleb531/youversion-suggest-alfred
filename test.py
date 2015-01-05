#!/usr/bin/env python
import unittest
import yv_suggest as yvs
import sys

class SearchBookTestCase(unittest.TestCase):
    '''Test the searching of Bible books'''

    def test_search_book_full(self):
        '''should match book by full name'''
        results = yvs.get_search_results('luke')
        self.assertEqual(results[0].title, 'Luke')

    def test_search_book_partial(self):
        '''should match book by partial name'''
        results = yvs.get_search_results('luk')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Luke')

    def test_search_book_case(self):
        '''should match book irrespective of case'''
        query = 'Luke'
        results = yvs.get_search_results(query)
        results_lower = yvs.get_search_results(query.lower())
        results_upper = yvs.get_search_results(query.upper())
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results_lower), 1)
        self.assertEqual(len(results_upper), 1)
        self.assertDictEqual(results[0].__dict__, results_lower[0].__dict__)

    def test_search_book_numbered_full(self):
        '''should match numbered book by full name'''
        results = yvs.get_search_results('1 corinthians')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, '1 Corinthians')

    def test_search_book_numbered_partial(self):
        '''should match numbered book by partial numbered name'''
        results = yvs.get_search_results('1 cor')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, '1 Corinthians')

    def test_search_book_numbered_partial(self):
        '''should match numbered book by partial non-numbered name'''
        results = yvs.get_search_results('cor')
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].title, '1 Corinthians')
        self.assertEqual(results[1].title, '2 Corinthians')

    def test_search_book_mixed(self):
        '''should match numbered and non-numbered books'''
        results = yvs.get_search_results('john')
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0].title, 'John')
        self.assertEqual(results[1].title, '1 John')
        self.assertEqual(results[2].title, '2 John')
        self.assertEqual(results[3].title, '3 John')

    def test_search_book_id(self):
        '''should use correct id for book'''
        results = yvs.get_search_results('luke')
        self.assertEqual(results[0].uid, 'luk.1.niv')

    def test_search_book_url(self):
        '''should use correct url for book'''
        results = yvs.get_search_results('luke')
        self.assertEqual(results[0].arg, 'https://www.bible.com/bible/' + results[0].uid)

    def test_search_book_nonexistent(self):
        '''should not match nonexistent book'''
        results = yvs.get_search_results('foo')
        self.assertEqual(len(results), 0)

class SearchChapterTestCase(unittest.TestCase):

    def test_search_chapter(self):
        '''should match chapter'''
        results = yvs.get_search_results('luke 4')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Luke 4')

    def test_search_chapter_id(self):
        '''should use correct id for chapter'''
        results = yvs.get_search_results('luke 4')
        self.assertEqual(len(results), 1)

    def test_search_chapter_nonexistent(self):
        '''should not match nonexistent chapter'''
        results = yvs.get_search_results('psalm 151')
        self.assertEqual(len(results), 0)

class SearchVerseTestCase(unittest.TestCase):

    def test_search_verse(self):
        '''should match verse'''
        results = yvs.get_search_results('luke 4:8')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Luke 4:8')

    def test_search_verse_dot(self):
        '''should match verse with dot separator'''
        results = yvs.get_search_results('luke 4.8')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Luke 4.8')

    def test_search_verse_dot(self):
        '''should use correct id for verse'''
        results = yvs.get_search_results('luke 4:8')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].uid, 'luk.4.8.niv')

class SearchVersionTestCase(unittest.TestCase):

    def test_search_version_full(self):
        '''should match version by full name'''
        results = yvs.get_search_results('luke 4:8 esv')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].subtitle, 'ESV')

    def test_search_version_numbered(self):
        '''should match version ending in number'''
        results = yvs.get_search_results('luke 4:8 rv1885')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].subtitle, 'RV1885')

    def test_search_version_case(self):
        '''should match version irrespective of case'''
        query = 'luke 4.8 esv'
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

    def test_search_version_partial_ambiguous(self):
        '''should match version by ambiguous partial name'''
        results = yvs.get_search_results('luke 4:8 a')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].subtitle, 'AMP')

if __name__ == '__main__':
    unittest.main(verbosity=2)
