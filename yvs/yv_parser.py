# yvs.yv_parser
# coding=utf-8

from __future__ import print_function, unicode_literals

from HTMLParser import HTMLParser

import yvs.shared as yvs


# A base class for parsing YouVersion HTML
class YVParser(HTMLParser):

    # Handle named character references; pass evaluated characters to
    # handle_data method to simplify the parsing of data between HTML tags
    def handle_entityref(self, name):
        self.handle_data(yvs.eval_html_charref(name))

    # Handle decimal and hexadecimal character references
    def handle_charref(self, name):
        self.handle_data(yvs.eval_html_charref(name))
