#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals
import re
import yvs.shared as shared
import urllib
from HTMLParser import HTMLParser


ref_url_prefix = '/bible/'


def get_uid_from_url(url):

    return url.replace(ref_url_prefix, '')


# Parser for search result HTML
class SearchResultParser(HTMLParser):

    # Reset parser variables (implicitly called on instantiation)
    def reset(self):
        HTMLParser.reset(self)
        self.in_ref = None
        self.in_heading = None
        self.in_content = None
        self.results = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if 'class' in attr_dict:
            elem_class = attr_dict['class']
            # Detect beginning of search result
            if tag == 'li' and elem_class == 'reference':
                self.in_ref = True
                self.currentResult = {
                    'arg': '',
                    'title': '',
                    'subtitle': ''
                }
                self.results.append(self.currentResult)
        # Detect beginning of search result heading
        if self.in_ref and tag == 'a':
            self.in_heading = True
            self.currentResult['arg'] = get_uid_from_url(attr_dict['href'])
        # Detect beginning of search result content
        elif self.in_ref and tag == 'p':
            self.in_content = True

    def handle_endtag(self, tag):
        if self.in_ref and tag == 'li':
            self.in_ref = False
        # Determine the end of a verse or its content
        elif self.in_heading and tag == 'a':
            self.in_heading = False
        elif self.in_content and tag == 'p':
            self.in_content = False
            self.currentResult['subtitle'] = shared.format_ref_content(
                self.currentResult['subtitle'])

    # Handle verse content
    def handle_data(self, content):
        if self.in_ref:
            if self.in_heading:
                self.currentResult['title'] += content
            elif self.in_content:
                self.currentResult['subtitle'] += content

    # Handle all non-ASCII characters encoded as HTML entities
    def handle_charref(self, name):
        if self.in_ref:
            char = shared.eval_charref(name)
            if self.in_heading:
                self.currentResult['title'] += char
            elif self.in_content:
                self.currentResult['subtitle'] += char


# Retrieve HTML for reference with the given ID
def get_search_html(query_str):

    prefs = shared.get_prefs()
    url = 'https://www.bible.com/search/bible?q={}&version_id={}'.format(
        urllib.quote_plus(query_str.encode('utf-8')), prefs['version'])
    return shared.get_url_content(url)


# Parse actual reference content from reference HTML
def get_result_list(query_str):

    query_str = shared.format_query_str(query_str)
    html = get_search_html(query_str)
    parser = SearchResultParser()
    parser.feed(html)
    return parser.results


def main(query_str):

    results = get_result_list(query_str)
    if not results:
        results = [{
            'uid': 'yvs-no-results',
            'title': 'No Results',
            'subtitle': 'No bible references matching \'{}\''
            .format(query_str),
            'valid': 'no'
        }]

    print(shared.get_result_list_xml(results))

if __name__ == '__main__':
    main('{query}')
