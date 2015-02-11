#!/usr/bin/env python
import unittest
import yv_suggest.open as yvs
import inspect


class WebbrowserMock(object):
    """mock the builtin webbrowser module"""

    def open(self, url):
        """mock the webbrowser.open() function"""
        self.url = url


class OpenTestCase(unittest.TestCase):
    """test the handling of Bible reference URLs"""

    def test_url(self):
        """should build correct URL to Bible reference"""
        url = yvs.get_ref_url('esv/jhn.3.16')
        self.assertEqual(url, 'https://www.bible.com/bible/esv/jhn.3.16')

    def test_query_param(self):
        """should use received query parameter as default ref ID"""
        spec = inspect.getargspec(yvs.main)
        default_query_str = spec.defaults[0]
        self.assertEqual(default_query_str, '{query}')

    def test_url_open(self):
        """should attempt to open URL using webbrowser module"""
        mock = WebbrowserMock()
        yvs.webbrowser = mock
        yvs.main('nlt/jhn.3.17')
        self.assertEqual(mock.url, 'https://www.bible.com/bible/nlt/jhn.3.17')

if __name__ == '__main__':
    unittest.main()
