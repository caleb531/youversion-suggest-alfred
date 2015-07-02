#!/usr/bin/env python

import re
import yvs.shared as shared
from HTMLParser import HTMLParser


# Parser for reference HTML
class ReferenceParser(HTMLParser):

    # Associates the given reference object with this parser instance
    def __init__(self, ref):
        HTMLParser.__init__(self)
        if 'verse' in ref:
            self.verse_start = ref['verse']
            if 'endverse' in ref:
                self.verse_end = ref['endverse']
            else:
                self.verse_end = self.verse_start
        else:
            self.verse_start = 1
            self.verse_end = None

    # Reset parser variables (implicitly called on instantiation)
    def reset(self):
        HTMLParser.reset(self)
        self.depth = 0
        self.in_block = None
        self.in_verse = None
        self.in_content = None
        self.block_depth = None
        self.verse_depth = None
        self.content_depth = None
        self.verse_num = None
        self.content_parts = []

    # Determines if parser is currently within content of verse to include
    def is_in_verse_content(self):
        return (self.in_verse and self.in_content and
                (self.verse_start <= self.verse_num and
                 (not self.verse_end or self.verse_num <= self.verse_end)))

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == 'div' or tag == 'span':
            self.depth += 1
        if 'class' in attr_dict:
            elem_class = attr_dict['class']
            # Detect paragraph breaks between verses
            if elem_class == 'p' or elem_class == 'b':
                self.in_block = True
                self.block_depth = self.depth
                self.content_parts.append('\n\n')
            # Detect line breaks within a single verse
            if elem_class == 'q1' or elem_class == 'q2' or elem_class == 'li1':
                self.content_parts.append('\n')
            # Detect beginning of a single verse (may include footnotes)
            if 'verse ' in elem_class:
                self.in_verse = True
                self.verse_depth = self.depth
                self.verse_num = int(elem_class.split(' ')[1][1:])
            # Detect beginning of verse content (excludes footnotes)
            if elem_class == 'content':
                self.in_content = True
                self.content_depth = self.depth

    def handle_endtag(self, tag):
        if self.depth == self.block_depth and self.in_block:
            self.in_block = False
            self.content_parts.append('\n')
        # Determine the end of a verse or its content
        if self.depth == self.verse_depth and self.in_verse:
            self.in_verse = False
        if self.depth == self.content_depth and self.in_content:
            self.in_content = False
        if tag == 'div' or tag == 'span':
            self.depth -= 1

    # Handle verse content
    def handle_data(self, content):
        if self.is_in_verse_content():
            self.content_parts.append(content)

    # Handle all non-ASCII characters encoded as HTML entities
    def handle_charref(self, name):
        if self.is_in_verse_content():
            char = shared.eval_charref(name)
            self.content_parts.append(char)


# Retrieve HTML for reference with the given ID
def get_ref_html(ref):
    url = 'https://www.bible.com/bible/{version}/{book}.{chapter}'.format(
        version=ref['version_id'],
        book=ref['book_id'],
        chapter=ref['chapter'])
    return shared.get_url_content(url)


# Parse actual reference content from reference HTML
def get_ref_content(ref):
    html = get_ref_html(ref)
    parser = ReferenceParser(ref)
    parser.feed(html)
    ref_content = shared.format_ref_content(''.join(parser.content_parts))
    ref_content = '\n\n' + ref_content
    ref_content = shared.get_full_ref(ref) + ref_content
    return ref_content


def main(ref_uid):
    ref = shared.get_ref_object(ref_uid)
    print(get_ref_content(ref).encode('utf-8'))

if __name__ == '__main__':
    main('{query}')
