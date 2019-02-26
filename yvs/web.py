#!/usr/bin/env python
# coding=utf-8

import urllib2
from gzip import GzipFile
from htmlentitydefs import name2codepoint
from StringIO import StringIO

# The user agent used for HTTP requests sent to the YouVersion website
USER_AGENT = 'YouVersion Suggest'
# The number of seconds to wait before timing out an HTTP request connection
REQUEST_CONNECTION_TIMEOUT = 3


# Retrieves HTML contents of the given URL as a Unicode string
def get_url_content(url):

    request = urllib2.Request(url, headers={
        'User-Agent': USER_AGENT,
        'Accept-Encoding': 'gzip, deflate'
    })
    response = urllib2.urlopen(request, timeout=REQUEST_CONNECTION_TIMEOUT)
    url_content = response.read()

    # Decompress response body if gzipped
    if response.info().get('Content-Encoding') == 'gzip':
        str_buf = StringIO(url_content)
        with GzipFile(fileobj=str_buf, mode='rb') as gzip_file:
            url_content = gzip_file.read()

    return url_content.decode('utf-8')


# Evaluates HTML character reference to its respective Unicode character
def eval_html_charref(name):

    if name[0] == 'x':
        # Handle hexadecimal character references
        return unichr(int(name[1:], 16))
    elif name.isdigit():
        # Handle decimal character references
        return unichr(int(name))
    else:
        # Otherwise, assume character reference is a named reference
        return unichr(name2codepoint[name])
