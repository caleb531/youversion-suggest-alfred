#!/usr/bin/env python
import unittest
import yv_suggest as yvs

class SearchVerseTestCase(unittest.TestCase):
    '''test the searching of Bible verses'''

    def test_search_verse(self):
        '''should match verses'''
        results = yvs.get_result_list('luke 4:8')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Luke 4:8')

    def test_search_chapter_ambig(self):
        '''should match verses by ambiguous book reference'''
        results = yvs.get_result_list('a 3:2')
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].title, 'Amos 3:2')
        self.assertEqual(results[1].title, 'Acts 3:2')

    def test_search_verse_dot(self):
        '''should match verses preceded by dot'''
        results = yvs.get_result_list('luke 4.8')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Luke 4.8')

    def test_search_verse_dot(self):
        '''should use correct ID for verses'''
        results = yvs.get_result_list('luke 4:8')
        self.assertEqual(results[0].uid, 'niv/luk.4.8')

if __name__ == '__main__':
    unittest.main()
