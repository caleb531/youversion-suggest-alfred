# utilities.book_parser
# coding=utf-8

from __future__ import unicode_literals

import re

import yvs.shared as shared
from yvs.yv_parser import YVParser


# Finds on the YouVersion website the ID and name of every Bible book in a
# particular Bible version
class BookParser(YVParser):

    # Resets parser variables (implicitly called on instantiation)
    def reset(self):
        YVParser.reset(self)
        self.depth = 0
        self.in_book_list = False
        self.book_list_depth = 0
        self.in_book = False
        self.book_depth = 0
        self.books = []
        self.book_name_parts = []

    # Detects the start of a book link
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.depth += 1
        if 'class' in attr_dict and 'book-list' in attr_dict['class']:
            self.in_book_list = True
            self.book_list_depth = self.depth
        elif self.in_book_list and tag == 'li':
            self.in_book = True
            self.book_depth = self.depth
            book_id_matches = re.search(
                r'\$([a-z]{3}|[1-3][a-z]{2})',
                attr_dict['data-reactid'].lower())
            self.books.append({
                'id': book_id_matches.group(1)
            })

    # Detects the end of a book link
    def handle_endtag(self, tag):
        if self.in_book and self.depth == self.book_depth:
            self.in_book = False
            self.books[-1]['name'] = ''.join(self.book_name_parts).strip()
            # Empty the list containing the book name parts
            del self.book_name_parts[:]
        if self.in_book_list and self.depth == self.book_list_depth:
            self.in_book_list = False
        self.depth -= 1

    # Handles the book name contained within the current book link
    def handle_data(self, data):
        if self.in_book:
            self.book_name_parts.append(data)


# Retrieves all books listed on the chapter page in the given default version
def get_books(default_version):

    page_html = shared.get_url_content(
        'https://www.bible.com/bible/{}/jhn.1'.format(default_version))

    parser = BookParser()
    parser.feed(page_html)

    return parser.books
