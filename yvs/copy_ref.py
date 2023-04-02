#!/usr/bin/env python3
# coding=utf-8

import json
import re
import sys

import yvs.core as core
import yvs.web as web


# An HTML parser which receives HTML from the page for a YouVersion
# Bible reference and parses it to construct a shareable plain text reference
class ReferenceParser(web.YVParser):

    # Elements that should be surrounded by blank lines
    block_elems = {'b', 'p', 'm'}
    # Elements that should trigger a line break
    break_elems = {'li1', 'q1', 'q2', 'qc', 'qm1', 'qm2'}

    # Associates the given reference object with this parser instance
    def __init__(self, ref,
                 include_verse_numbers=False, include_line_breaks=False):
        super().__init__()
        if 'verse' in ref:
            # If reference is a verse or verse range, set the correct range of
            # verses to copy
            self.verse_start = ref['verse']
            self.verse_end = ref.get('endverse', self.verse_start)
        else:
            # Otherwise, assume reference is a chapter
            self.verse_start = 1
            self.verse_end = None
        self.include_verse_numbers = include_verse_numbers
        self.include_line_breaks = include_line_breaks

    # Resets parser variables (implicitly called when parser is instantiated)
    def reset(self):
        super().reset()
        self.depth = 0
        self.in_block = False
        self.in_verse = False
        self.in_verse_label = False
        self.in_verse_content = False
        self.in_verse_note = False
        self.block_depth = 0
        self.verse_depth = 0
        self.label_depth = 0
        self.content_depth = 0
        self.verse_nums = []
        self.content_parts = []

    # Returns True if parser is currently within the a verse to include
    # (otherwise, returns False)
    def is_in_verse(self):
        return any(self.in_verse and
                   (verse_num >= self.verse_start and
                    (not self.verse_end or verse_num <= self.verse_end))
                   for verse_num in self.verse_nums)

    # Returns True if parser is currently within the content of a verse to
    # include
    def is_in_verse_content(self):
        return (self.is_in_verse() and self.in_verse_content
                and not self.in_verse_note)

    # Returns True if parser is currently within the label of a verse to
    # include (otherwise, returns False)
    def is_in_verse_label(self):
        return (self.is_in_verse() and self.include_verse_numbers and
                self.in_verse_label and not self.in_verse_note)

    # Return True if the given class name matches one of the patterns defined in
    # the supplied elements set; matching is done literally and on word
    # boundaries (e.g. so the class "ChapterContent_q1__ZQPnV" matches if "q1"
    # is in the elements set)
    def class_matches_oneof(self, class_name, elems_set):
        elems_union = '|'.join(elems_set)
        # The normal regex word boundary (\b) considers underscores as part of
        # the definition of a "word"; this will not work for us since the class
        # names we are working with have underscore-delimited components, and we
        # need to treat each of those components as distinct "words";
        # fortunately, we can use negative lookbehinds/lookaheads to effectively
        # implement a custom word boundary, per this blog post:
        # <http://www.rexegg.com/regex-boundaries.html#diy>
        word_patt = '[A-Za-z0-9]'
        return bool(re.search(rf'(?<!{word_patt})({elems_union})(?!{word_patt})', class_name))

    # Detects the start of blocks, breaks, verses, and verse content
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        # Keep track of element depth throughout entire document
        self.depth += 1
        # We can't just use the Python 'in' operator to check if the key
        # exists, because it's perfectly valid for an HTML element to have a
        # attribute name present, but without any value (e.g. <div class>); in
        # this case, the attrs dictionary would have a 'class' attribute with a
        # value of None
        elem_class = attrs.get('class')
        if not elem_class:
            return
        elem_class_names = elem_class.split(' ')
        # Detect paragraph breaks between verses
        if self.class_matches_oneof(elem_class, self.block_elems):
            self.in_block = True
            self.block_depth = self.depth
            self.content_parts.append(
                '\n\n' if self.include_line_breaks else ' ')
        # Detect line breaks within a single verse
        if self.class_matches_oneof(elem_class, self.break_elems):
            self.content_parts.append(
                '\n' if self.include_line_breaks else ' ')
        # Detect beginning of a single verse (may include footnotes)
        if self.class_matches_oneof(elem_class, {'verse'}):
            self.in_verse = True
            self.verse_depth = self.depth
            self.verse_nums = [int(class_name[1:])
                               for class_name in elem_class_names[1:]]
        # Detect label containing the associated verse number(s)
        if self.class_matches_oneof(elem_class, {'label'}):
            self.in_verse_label = True
            self.label_depth = self.depth
        # Detect beginning of verse content (excludes footnotes)
        if self.class_matches_oneof(elem_class, {'content'}):
            self.in_verse_content = True
            self.content_depth = self.depth
        # Detect footnotes and cross-references
        if self.class_matches_oneof(elem_class, {'note'}):
            self.in_verse_note = True
            self.note_depth = self.depth

    # Detects the end of blocks, breaks, verses, and verse content
    def handle_endtag(self, tag):
        if self.in_block and self.depth == self.block_depth:
            self.in_block = False
            self.content_parts.append(
                '\n' if self.include_line_breaks else ' ')
        elif self.in_verse and self.depth == self.verse_depth:
            self.in_verse = False
        elif self.in_verse_label and self.depth == self.label_depth:
            self.in_verse_label = False
        elif self.in_verse_content and self.depth == self.content_depth:
            self.in_verse_content = False
        elif self.in_verse_note and self.depth == self.note_depth:
            self.in_verse_note = False
        self.depth -= 1

    # Handles verse labels and content
    def handle_data(self, data):
        if self.is_in_verse_label():
            self.content_parts.append(' {} '.format(data.strip()))
        if self.is_in_verse_content():
            self.content_parts.append(data)


# Retrieves the UID of the chapter to which this reference belongs
def get_ref_chapter_uid(ref):

    return '{version}/{book}.{chapter}'.format(
        version=ref['version_id'],
        book=ref['book_id'],
        chapter=ref['chapter'])


# Retrieves HTML for of the chapter to which the reference belongs
def get_chapter_html(ref, revalidate=False):

    chapter_uid = get_ref_chapter_uid(ref)
    url = core.get_ref_url(ref_uid=chapter_uid)
    entry_key = '{}.html'.format(chapter_uid)

    return web.get_url_content_with_caching(
        url,
        entry_key,
        revalidate=revalidate)


# Parses actual reference content from chapter HTML
def get_formatted_ref_content(ref, ref_format,
                              include_verse_numbers, include_line_breaks):

    parser = ReferenceParser(
        ref,
        include_verse_numbers=include_verse_numbers,
        include_line_breaks=include_line_breaks)

    web.get_and_parse_html(
        parser=parser,
        html_getter=get_chapter_html,
        html_getter_args=(ref,),
        parser_results_attr='content_parts')

    # Format reference content by removing superfluous whitespace and such
    ref_content = core.normalize_ref_content(''.join(parser.content_parts))

    if ref_content:
        formatted_ref_content = ref_format.format(
            name=core.get_basic_ref_name(ref),
            version=ref['version'],
            content=ref_content,
            url=core.get_ref_url(ref['uid']))
        return formatted_ref_content
    else:
        return ''


# Retrieves reference content using the given reference object and preferences
def get_copied_ref_from_object(ref, user_prefs):

    return get_formatted_ref_content(
        ref,
        ref_format=user_prefs['refformat'],
        include_verse_numbers=user_prefs['versenumbers'],
        include_line_breaks=user_prefs['linebreaks'])


# Retrieves entire reference (header and content) to be copied
def get_copied_ref(ref_uid):

    user_prefs = core.get_user_prefs()
    ref = core.get_ref(ref_uid, user_prefs)
    return get_copied_ref_from_object(ref, user_prefs)


def main(ref_uid):

    user_prefs = core.get_user_prefs()
    ref = core.get_ref(ref_uid, user_prefs)
    print(json.dumps({
        'alfredworkflow': {
            'arg': ref_uid,
            'variables': {
                'copied_ref': get_copied_ref_from_object(ref, user_prefs),
                'full_ref_name': core.get_full_ref_name(ref)
            }
        }
    }))


if __name__ == '__main__':
    main(sys.argv[1])
