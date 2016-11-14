# yvs.yv_parser
# coding=utf-8

from __future__ import unicode_literals

from HTMLParser import HTMLParser

import yvs.shared as yvs


# A base class for parsing YouVersion HTML
class YVParser(HTMLParser):

    # Pass character references to handle_data method to simplify the parsing
    # of data between HTML tags
    def handle_charref(self, name):
        self.handle_data(yvs.eval_html_charref(name))
