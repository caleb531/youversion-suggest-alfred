#!/usr/bin/env python

from __future__ import print_function
import re
import urllib2
import shared
from HTMLParser import HTMLParser


# Retrieve HTML for reference with the given ID
def get_ref_html(ref_uid):
    url = 'https://www.bible.com/bible/{}'.format(ref_uid)
    return urllib2.urlopen(url).read()


# Parser for reference HTML
class ReferenceParser(HTMLParser):

    level = 0
    in_block = False
    in_verse = False
    in_content = False
    block_depth = None
    verse_depth = None
    content_depth = None
    ref_text = ''

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == 'div' or tag == 'span':
            self.level += 1
        if 'class' in attr_dict:
            div_class = attr_dict['class']
            if div_class == 'p' or re.match('q\d+', div_class):
                self.in_block = True
                self.block_depth = self.level
                self.ref_text += '\n'
            if re.match('s\d+', div_class):
                self.ref_text += '\n'
            if 'verse' in div_class:
                self.in_verse = True
                self.verse_depth = self.level
            if div_class == 'content':
                self.in_content = True
                self.content_depth = self.level

    def handle_endtag(self, tag):
        # Determine when certain classes of elements end
        if self.level == self.block_depth:
            self.in_block = False
        if self.level == self.verse_depth:
            self.in_verse = False
            # Ensure that a space separates consecutive sentences
            self.ref_text += ' '
        if self.level == self.content_depth:
            self.in_content = False
        if tag == 'div' or tag == 'span':
            self.level -= 1

    def handle_data(self, content):
        if self.in_verse and self.in_content and content.strip() != '':
            self.ref_text += content

    def handle_charref(self, name):
        if self.in_verse and self.in_content:
            if name[0] == 'x':
                # Handle hexadecimal character references
                self.ref_text += unichr(int(name[1:], 16))
            else:
                # Handle decimal character references
                self.ref_text += unichr(int(name))


# Parse actual reference content from reference HTML
def get_ref_text(html):
    parser = ReferenceParser()
    parser.feed(html)
    return format_ref_text(parser.ref_text)


def format_ref_text(ref_text):
    # Collapse spaces
    ref_text = re.sub(' +', ' ', ref_text)
    # Strip any leading or trailing whitespace
    ref_text = re.sub('(^\s+)|(\s+$)', '', ref_text)
    return ref_text


def main(ref_uid):
    ref_text = shared.get_full_ref(shared.get_ref_object(ref_uid))
    ref_text += '\n\n'
    ref_text += get_ref_text(get_ref_html(ref_uid))
    print(ref_text)

if __name__ == '__main__':
    main('{query}')
