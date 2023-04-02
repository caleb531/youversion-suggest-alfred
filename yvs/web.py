#!/usr/bin/env python3
# coding=utf-8

import re
import urllib.request
from gzip import GzipFile
from html.parser import HTMLParser
from io import BytesIO

import yvs.cache as cache

# The user agent used for HTTP requests sent to the YouVersion website
USER_AGENT = 'YouVersion Suggest'
# The number of seconds to wait before timing out an HTTP request connection
REQUEST_CONNECTION_TIMEOUT = 5


# Optimizes HTML contents from YouVersion to omit large <script> tags and other
# things
def optimize_html(html):
    html = re.sub(r'<script(.*?)>(.*?)</script>', '', html)
    return html


# Retrieves HTML contents of the given URL as a Unicode string
def get_url_content(url):

    request = urllib.request.Request(url, headers={
        'User-Agent': USER_AGENT,
        'Accept-Encoding': 'gzip, deflate'
    })
    response = urllib.request.urlopen(
        request,
        timeout=REQUEST_CONNECTION_TIMEOUT)
    url_content = response.read()

    # Decompress response body if gzipped
    if response.info().get('Content-Encoding') == 'gzip':
        str_buf = BytesIO(url_content)
        with GzipFile(fileobj=str_buf, mode='rb') as gzip_file:
            url_content = gzip_file.read().decode('utf-8')

    return url_content


# Retrieve HTML contents of the given URL
def get_url_content_with_caching(url, entry_key, *, revalidate=False):

    # If revalidate is True, then we should skip lookup of cached HTML, fetch
    # latest the HTML directly from server, and cache that new HTML
    if revalidate:
        html = None
    else:
        html = cache.get_cache_entry_content(entry_key)

    # If revalidate is True OR if there is a cache-miss, then fetch the latest
    # HTML from YouVersion
    if not html:
        html = optimize_html(get_url_content(url))
        cache.add_cache_entry(entry_key, html)

    return html


# A base class for parsing YouVersion HTML
class YVParser(HTMLParser):

    pass


# A utility that consolidates the logic used to fetch and parse YouVersion HTML
# in a way that complements the caching mechanism built into this workflow; for
# example,
def get_and_parse_html(
    *,
    parser,              # An instance of an HTMLParser subclass
    html_getter,         # A function that retrieves the HTML
                         # to parse; this function should accept a
                         # 'revalidate' boolean parameter
    html_getter_args,    # An iterable of any initial arguments
                         # to the html_getter function
    parser_results_attr  # The name of the attribute on the HTMLParser object
                         # that represents the results of the parsing; ideally,
                         # this should be a sequence or string so that a falsy
                         # value indicates emptiness
):

    parser_exception = None
    try:
        parser.feed(html_getter(*html_getter_args))
    except Exception as exception:
        # Silently ignore exceptions encountered when parsing the cached HTML
        parser_exception = exception

    # If cached HTML returns no results, or if cached HTML produces an error
    # while parsing, attempt to fetch the latest HTML from YouVersion (this is
    # the 'revalidate' case)
    if parser_exception or not getattr(parser, parser_results_attr):
        parser.reset()
        parser.feed(html_getter(*html_getter_args, revalidate=True))

    return getattr(parser, parser_results_attr)
