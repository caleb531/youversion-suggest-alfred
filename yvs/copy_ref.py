#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function, unicode_literals

import json
import sys

import yvs.core as core
import yvs.cache as cache
import yvs.web as web
from yvs.yv_parser import YVParser

# Elements that should be surrounded by blank lines
BLOCK_ELEMS = {'b', 'p', 'm'}
# Elements that should trigger a line break
BREAK_ELEMS = {'li1', 'q1', 'q2', 'qc'}


# An HTML parser which receives HTML from the page for a YouVersion
# Bible reference and parses it to construct a shareable plain text reference
class ReferenceParser(YVParser):

    # Associates the given reference object with this parser instance
    def __init__(self, ref):
        YVParser.__init__(self)
        if 'verse' in ref:
            # If reference is a verse or verse range, set the correct range of
            # verses to copy
            self.verse_start = ref['verse']
            self.verse_end = ref.get('endverse', self.verse_start)
        else:
            # Otherwise, assume reference is a chapter
            self.verse_start = 1
            self.verse_end = None

    # Resets parser variables (implicitly called when parser is instantiated)
    def reset(self):
        YVParser.reset(self)
        self.depth = 0
        self.in_block = False
        self.in_verse = False
        self.in_verse_content = False
        self.block_depth = 0
        self.verse_depth = 0
        self.content_depth = 0
        self.verse_num = None
        self.content_parts = []

    # Returns True if parser is currently within the content of a verse to
    # include (otherwise, returns False)
    def is_in_verse_content(self):
        return (self.in_verse and self.in_verse_content and
                (self.verse_num >= self.verse_start and
                 (not self.verse_end or self.verse_num <= self.verse_end)))

    # Detects the start of blocks, breaks, verses, and verse content
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        # Keep track of element depth throughout entire document
        self.depth += 1
        if 'class' in attr_dict:
            elem_class = attr_dict['class']
            elem_class_names = elem_class.split(' ')
            # Detect paragraph breaks between verses
            if elem_class in BLOCK_ELEMS:
                self.in_block = True
                self.block_depth = self.depth
                self.content_parts.append('\n\n')
            # Detect line breaks within a single verse
            if elem_class in BREAK_ELEMS:
                self.content_parts.append('\n')
            # Detect beginning of a single verse (may include footnotes)
            if 'verse' in elem_class_names:
                self.in_verse = True
                self.verse_depth = self.depth
                self.verse_num = int(elem_class_names[1][1:])
            # Detect beginning of verse content (excludes footnotes)
            if elem_class == 'content':
                self.in_verse_content = True
                self.content_depth = self.depth

    # Detects the end of blocks, breaks, verses, and verse content
    def handle_endtag(self, tag):
        if self.in_block and self.depth == self.block_depth:
            self.in_block = False
            self.content_parts.append('\n')
        elif self.in_verse and self.depth == self.verse_depth:
            self.in_verse = False
        elif self.in_verse_content and self.depth == self.content_depth:
            self.in_verse_content = False
        self.depth -= 1

    # Handles verse content
    def handle_data(self, data):
        if self.is_in_verse_content():
            self.content_parts.append(data)


# Retrieves the UID of the chapter to which this reference belongs
def get_ref_chapter_uid(ref):

    return '{version}/{book}.{chapter}'.format(
        version=ref['version_id'],
        book=ref['book_id'],
        chapter=ref['chapter'])


# Retrieves HTML for of the chapter to which the reference belongs
def get_chapter_html(ref):

    chapter_uid = get_ref_chapter_uid(ref)
    url = core.get_ref_url(ref_uid=chapter_uid)

    entry_key = '{}.html'.format(chapter_uid)
    chapter_html = cache.get_cache_entry_content(entry_key)
    if not chapter_html:
        chapter_html = web.get_url_content(url)
        cache.add_cache_entry(entry_key, chapter_html)

    return chapter_html


# Parses actual reference content from chapter HTML
def get_ref_content(ref, ref_format):

    chapter_html = get_chapter_html(ref)
    parser = ReferenceParser(ref)
    parser.feed(chapter_html)
    # Format reference content by removing superfluous whitespace and such
    ref_content = core.normalize_ref_content(
        ''.join(parser.content_parts))

    if ref_content:
        copied_content = ref_format.format(
            name=core.get_basic_ref_name(ref),
            version=ref['version'],
            content=ref_content,
            url=core.get_ref_url(ref['uid']))
        return copied_content
    else:
        return ''


# Retrieves entire reference (header and content) to be copied
def get_copied_ref(ref_uid):

    user_prefs = core.get_user_prefs()
    ref = core.get_ref(ref_uid, user_prefs)
    return get_ref_content(ref, ref_format=user_prefs['refformat'])


def main(ref_uid):

    print(json.dumps({
        'alfredworkflow': {
            'arg': ref_uid,
            'variables': {
                'copied_ref': get_copied_ref(ref_uid)
            }
        }
    }))


if __name__ == '__main__':
    main(sys.argv[1].decode('utf-8'))
