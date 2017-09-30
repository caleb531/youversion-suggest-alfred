# utilities.version_parser
# coding=utf-8

from __future__ import unicode_literals

import re

import yvs.shared as shared
from yvs.yv_parser import YVParser


# Finds on the YouVersion website the ID and name of every Bible version in a
# particular YouVersion-supported language
class VersionParser(YVParser):

    # Resets parser variables (implicitly called on instantiation)
    def reset(self):
        YVParser.reset(self)
        self.depth = 0
        self.in_version = False
        self.version_depth = 0
        self.versions = []
        self.version_content_parts = []

    # Detects the start of a version link
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.depth += 1
        if 'href' in attr_dict:
            patt = r'(?<=/versions/)(\d+)-([a-z]+\d*)'
            matches = re.search(patt, attr_dict['href'], flags=re.UNICODE)
            if matches:
                self.in_version = True
                self.version_depth = self.depth
                self.versions.append({
                    'id': int(matches.group(1))
                })

    # Parse the version name from the accumulated version content
    def get_version_name(self):
        version_content = ''.join(self.version_content_parts).strip()
        matches = re.search(r'\(\s*([^\)]+)\s*\)\s*$', version_content)
        return matches.group(1)

    # Detects the end of a version link
    def handle_endtag(self, tag):
        if self.in_version and self.depth == self.version_depth:
            self.in_version = False
            self.versions[-1]['name'] = self.get_version_name().strip()
            # Empty the list containing the version name parts
            del self.version_content_parts[:]
        self.depth -= 1

    # Handles the version name contained within the current version link
    def handle_data(self, data):
        if self.in_version:
            self.version_content_parts.append(data)


# Retrieves all versions listed on the chapter page in the given language code
def get_versions(language_id):

    page_html = shared.get_url_content(
        'https://www.bible.com/languages/{}'.format(language_id))

    parser = VersionParser()
    parser.feed(page_html)

    return parser.versions
