#!/usr/bin/env python
import unittest
import yv_suggest.search as yvs
from xml.etree import ElementTree as ET
from contextlib import contextmanager
from StringIO import StringIO
import inspect
import sys

class SearchMainTestCase(unittest.TestCase):
    '''test the main search function called by the workflow'''

    @contextmanager
    def redirect_stdout(self):
        '''temporarily redirect stdout to new output stream'''
        original_stdout = sys.stdout
        out = StringIO()
        try:
            sys.stdout = out
            yield out
        finally:
            sys.stdout = original_stdout

    def test_output(self):
        '''should output result list XML'''
        query_str = 'genesis 50:20'
        with self.redirect_stdout() as out:
            yvs.main(query_str)
            output = out.getvalue().strip()
            results = yvs.get_result_list(query_str)
            xml = yvs.get_result_list_xml(results).strip()
            self.assertEqual(output, xml)

    def test_null_result(self):
        '''should output "No Results" XML item for empty result lists'''
        query_str = 'nothing'
        with self.redirect_stdout() as out:
            yvs.main(query_str)
            xml = out.getvalue().strip()
            root = ET.fromstring(xml)
            item = root.find('item')
            self.assertIsNotNone(item, '<item> element is missing')
            self.assertEqual(item.get('valid'), 'no')
            title = item.find('title')
            self.assertEqual(title.text, 'No Results')

    def test_query_param(self):
        '''should use typed Alfred query as default query string'''
        spec = inspect.getargspec(yvs.main)
        default_query_str = spec.defaults[0]
        self.assertEqual(default_query_str, '{query}')

if __name__ == '__main__':
    unittest.main()
