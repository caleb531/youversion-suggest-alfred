#!/usr/bin/env python3
# coding=utf-8

from html.parser import HTMLParser


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
