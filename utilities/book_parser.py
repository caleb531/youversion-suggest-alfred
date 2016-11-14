# utilities.book_parser
# coding=utf-8

from __future__ import unicode_literals

import yvs.shared as shared
from yvs.yv_parser import YVParser


# Finds on the YouVersion website the ID and name of every Bible book in a
# particular Bible version
class BookParser(YVParser):

    # Resets parser variables (implicitly called on instantiation)
    def reset(self):
        YVParser.reset(self)
        self.depth = 0
        self.in_book = False
        self.book_depth = 0
        self.books = []
        self.book_name_parts = []

    # Detects the start of a book link
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.depth += 1
        if 'data-book' in attr_dict:
            self.in_book = True
            self.book_depth = self.depth
            self.books.append({
                'id': attr_dict['data-book']
            })

    # Detects the end of a book link
    def handle_endtag(self, tag):
        if self.in_book and self.depth == self.book_depth:
            self.in_book = False
            self.books[-1]['name'] = ''.join(self.book_name_parts).strip()
            # Empty the list containing the book name parts
            del self.book_name_parts[:]
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
