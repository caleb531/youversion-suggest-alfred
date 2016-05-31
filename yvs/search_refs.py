# yvs.search_refs
# coding=utf-8

from __future__ import unicode_literals
import urllib
import yvs.shared as shared
from HTMLParser import HTMLParser


REF_URL_PREFIX = '/bible/'


# Parses unique reference identifier from the given reference URL
def get_uid_from_url(url):

    return url.replace(REF_URL_PREFIX, '')


# Parser for search result HTML
class SearchResultParser(HTMLParser):

    # Resets parser variables (implicitly called on instantiation)
    def reset(self):
        HTMLParser.reset(self)
        self.in_ref = None
        self.in_heading = None
        self.in_content = None
        self.results = []
        self.current_result = None

    # Detects the start of search results, titles, reference content, etc.
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if 'class' in attr_dict:
            elem_class = attr_dict['class']
            # Detect beginning of search result
            if tag == 'li' and elem_class == 'reference':
                self.in_ref = True
                self.current_result = {
                    'arg': '',
                    'title': '',
                    'subtitle': ''
                }
                self.results.append(self.current_result)
        if self.in_ref:
            # Detect beginning of search result heading
            if tag == 'a':
                self.in_heading = True
                self.current_result['arg'] = get_uid_from_url(
                    attr_dict['href'])
            # Detect beginning of search result content
            elif tag == 'p':
                self.in_content = True

    # Detects the end of search results, titles, reference content, etc.
    def handle_endtag(self, tag):
        if self.in_ref:
            if tag == 'li':
                self.in_ref = False
            elif self.in_heading and tag == 'a':
                self.in_heading = False
            elif self.in_content and tag == 'p':
                self.in_content = False
                self.current_result['subtitle'] = shared.format_ref_content(
                    self.current_result['subtitle'])

    # Handles verse content
    def handle_data(self, content):
        if self.in_ref:
            if self.in_heading:
                self.current_result['title'] += content
            elif self.in_content:
                self.current_result['subtitle'] += content

    # Handles all non-ASCII characters encoded as HTML entities
    def handle_charref(self, name):
        if self.in_ref:
            char = shared.eval_html_charref(name)
            if self.in_heading:
                self.current_result['title'] += char
            elif self.in_content:
                self.current_result['subtitle'] += char


# Retrieves HTML for reference with the given ID
def get_search_html(query_str):

    version = shared.get_user_prefs()['version']
    url = 'https://www.bible.com/search/bible?q={}&version_id={}'.format(
        urllib.quote_plus(query_str.encode('utf-8')), version)

    return shared.get_url_content(url)


# Parses actual reference content from reference HTML
def get_result_list(query_str):

    query_str = shared.format_query_str(query_str)
    html = get_search_html(query_str)
    parser = SearchResultParser()
    parser.feed(html)
    return parser.results


def main(query_str):

    entry_key = 'yvsearch {}.json'.format(shared.format_query_str(query_str))
    feedback_str = shared.get_cache_entry_content(entry_key)
    if feedback_str is None:

        results = get_result_list(query_str)
        if not results:
            results.append({
                'title': 'No Results',
                'subtitle': 'No references matching \'{}\''.format(query_str),
                'valid': 'no'
            })

        feedback_str = shared.get_result_list_feedback_str(results)
        shared.add_cache_entry(entry_key, feedback_str)

    print(feedback_str.encode('utf-8'))


if __name__ == '__main__':
    main('{query}')
