# utilities.version_parser
# coding=utf-8

from __future__ import unicode_literals
import re
import yvs.shared as shared
from HTMLParser import HTMLParser


class VersionParser(HTMLParser):

    # Resets parser variables (implicitly called on instantiation)
    def reset(self):
        HTMLParser.reset(self)
        self.depth = 0
        self.in_version = False
        self.version_depth = 0
        self.versions = []
        self.version_name_parts = []

    # Parses the version ID from the given version URL
    def get_version_id(self, version_url):
        patt = r'(?<=/versions/)(\d+)-([a-z]+\d*)'
        matches = re.search(patt, version_url, flags=re.UNICODE)
        return {
            'id': int(matches.group(1)),
            'name': matches.group(2).upper(),
        }

    # Detects the start of a version link
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.depth += 1
        if '/versions/' in attr_dict['href']:
            self.in_version = True
            self.version_depth = self.depth
            self.versions.append({
                'id': attr_dict['href']
            })

    # Detects the end of a version link
    def handle_endtag(self, tag):
        if self.in_version and self.depth == self.version_depth:
            self.in_version = False
            self.versions[-1]['name'] = ''.join(
                self.version_name_parts).strip()
            # Empty the list containing the version name parts
            del self.version_name_parts[:]
        self.depth -= 1

    # Handles the version name contained within the current version link
    def handle_data(self, content):
        if self.in_version:
            self.version_name_parts.append(content)

    # Handles all HTML entities within the version name
    def handle_charref(self, name):
        if self.in_version:
            char = shared.eval_html_charref(name)
            self.version_name_parts.append(char)


# Retrieves all versions listed on the chapter page in the given language code
def get_versions(language_id):

    page_html = shared.get_url_content(
        'https://www.bible.com/languages/{}'.format(
            language_id.replace('_', '-')))

    parser = VersionParser()
    parser.feed(page_html)

    return parser.versions
