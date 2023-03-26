#!/usr/bin/env python3
# coding=utf-8

import sys
import urllib.parse

import yvs.core as core
import yvs.cache as cache
import yvs.web as web
from yvs.yv_parser import YVParser


# Parses unique reference identifier from the given reference URL
def get_uid_from_url(url):

    return (url
            .replace(core.BASE_REF_URL, '')
            # Handle case where origin may be absent from 'href' value
            .replace(urllib.parse.urlparse(core.BASE_REF_URL).path, ''))


# Parser for search result HTML
class SearchResultParser(YVParser):

    def __init__(self, user_prefs):
        YVParser.__init__(self)
        self.user_prefs = user_prefs

    # Resets parser variables (implicitly called on instantiation)
    def reset(self):
        YVParser.reset(self)
        self.depth = 0
        self.in_ref = False
        self.in_heading = False
        self.in_content = False
        self.content_depth = 0
        self.results = []
        self.current_result = None

    # Detects the start of search results, titles, reference content, etc.
    def handle_starttag(self, tag, attrs):
        self.depth += 1
        attrs = dict(attrs)
        # Detect beginning of search result
        if tag == 'a' and '/bible/' in attrs.get('href', ''):
            self.in_ref = True
            self.current_result = {
                'arg': '',
                'title': '',
                'subtitle': ''
            }
            self.results.append(self.current_result)
            self.in_heading = True
            self.current_result['arg'] = get_uid_from_url(attrs['href'])
            self.current_result['variables'] = {
                'ref_url': core.get_ref_url(self.current_result['arg']),
                'copybydefault': str(self.user_prefs['copybydefault'])
            }
            self.current_result['quicklookurl'] = \
                self.current_result['variables']['ref_url']
            self.current_result['mods'] = {
                'cmd': {
                    'subtitle': 'Copy content to clipboard'
                }
            }
            # Make "Copy" the default action (instead of "View") when the
            # copybydefault preference is set to true
            if self.user_prefs['copybydefault']:
                self.current_result['mods']['cmd']['subtitle'] = \
                    'View on YouVersion'
        # Detect beginning of search result content
        elif attrs.get('class') == 'content':
            self.in_content = True
            self.content_depth = self.depth

    # Detects the end of search results, titles, reference content, etc.
    def handle_endtag(self, tag):
        if self.in_ref and tag == 'p':
            self.in_ref = False
            self.current_result['subtitle'] = core.normalize_ref_content(
                self.current_result['subtitle'])
        elif self.in_heading and tag == 'a':
            self.in_heading = False
        elif self.in_content and tag == 'span' and self.depth == self.content_depth:
            self.in_content = False
        self.depth -= 1

    # Handles verse content
    def handle_data(self, data):
        if self.in_ref:
            if self.in_heading:
                self.current_result['title'] += data
            elif self.in_content:
                self.current_result['subtitle'] += data


# Retrieves HTML for reference with the given ID
def get_search_html(query_str, user_prefs):

    url = 'https://www.bible.com/search/bible?q={}&version_id={}'.format(
        urllib.parse.quote_plus(query_str), user_prefs['version'])

    entry_key = '{}/{}.html'.format(user_prefs['version'], query_str)
    search_html = cache.get_cache_entry_content(entry_key)
    if not search_html:
        search_html = web.get_url_content(url)
        cache.add_cache_entry(entry_key, search_html)

    return search_html


# Parses actual reference content from reference HTML
def get_result_list(query_str):

    query_str = core.normalize_query_str(query_str)
    user_prefs = core.get_user_prefs()
    html = get_search_html(query_str, user_prefs)
    parser = SearchResultParser(user_prefs)
    parser.feed(html)
    return parser.results


def main(query_str):

    results = get_result_list(query_str)
    if not results:
        results.append({
            'title': 'No Results',
            'subtitle': 'No references matching \'{}\''.format(query_str),
            'valid': False
        })

    print(core.get_result_list_feedback_str(results))


if __name__ == '__main__':
    main(sys.argv[1])
