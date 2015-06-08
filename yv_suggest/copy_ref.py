#!/usr/bin/env python

import re
import urllib2
import shared
from HTMLParser import HTMLParser


# Retrieve HTML for reference with the given ID
def get_ref_html(ref_uid):
    url = 'https://www.bible.com/bible/{}'.format(ref_uid)
    return urllib2.urlopen(url).read().decode('utf-8')


# Parser for reference HTML
class ReferenceParser(HTMLParser):

    level = 0
    in_verse = False
    in_content = False
    verse_depth = None
    content_depth = None
    ref_parts = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == 'div' or tag == 'span':
            self.level += 1
        if 'class' in attr_dict:
            div_class = attr_dict['class']
            if div_class == 'p':
                self.ref_parts.append('\n\n')
            if re.match('q\d+', div_class):
                self.ref_parts.append('\n')
            if 'verse' in div_class:
                self.in_verse = True
                self.verse_depth = self.level
            if div_class == 'content':
                self.in_content = True
                self.content_depth = self.level

    def handle_endtag(self, tag):
        # Determine when certain classes of elements end
        if self.level == self.verse_depth:
            self.in_verse = False
            # Ensure that a space separates consecutive sentences
            self.ref_parts.append(' ')
        if self.level == self.content_depth:
            self.in_content = False
        if tag == 'div' or tag == 'span':
            self.level -= 1

    def handle_data(self, content):
        if self.in_verse and self.in_content and content.strip() != '':
            self.ref_parts.append(content)

    def handle_charref(self, name):
        if self.in_verse and self.in_content:
            if name[0] == 'x':
                # Handle hexadecimal character references
                self.ref_parts.append(unichr(int(name[1:], 16)))
            else:
                # Handle decimal character references
                self.ref_parts.append(unichr(int(name)))


# Parse actual reference content from reference HTML
def get_ref_text(ref_uid, html):
    parser = ReferenceParser()
    parser.feed(html)
    ref_text = format_ref_text(''.join(parser.ref_parts))
    ref_text = '\n\n' + ref_text
    ref_text = shared.get_full_ref(shared.get_ref_object(ref_uid)) + ref_text
    return ref_text


def format_ref_text(ref_text):
    # Collapse consecutive spaces to single space
    ref_text = re.sub(' +', ' ', ref_text)
    # Collapse sequences of three or more newlines into two
    ref_text = re.sub('\n{2,}', '\n\n', ref_text)
    # Strip leading/trailing whitespace for entire reference
    ref_text = re.sub('(^\s+)|(\s+$)', '', ref_text)
    # Strip leading/trailing whitespace for each paragraph
    ref_text = re.sub('(\n +)|( +\n)', '\n', ref_text)
    return ref_text


def main(ref_uid):
    print(get_ref_text(ref_uid, get_ref_html(ref_uid)))

if __name__ == '__main__':
    main('{query}')
