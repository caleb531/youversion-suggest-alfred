# utilities.version_parser
# coding=utf-8

from __future__ import unicode_literals
import re
import yvs.shared as shared
from HTMLParser import HTMLParser


# Finds on the YouVersion website the ID and name of every Bible version in a
# particular YouVersion-supported language
class VersionParser(HTMLParser):

    # Resets parser variables (implicitly called on instantiation)
    def reset(self):
        HTMLParser.reset(self)
        self.versions = []

    # Detects the start of a version link
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if 'href' in attr_dict:
            patt = r'(?<=/versions/)(\d+)-([a-z]+\d*)'
            matches = re.search(patt, attr_dict['href'], flags=re.UNICODE)
            if matches:
                self.versions.append({
                    'id': int(matches.group(1)),
                    'name': matches.group(2).upper(),
                })


# Retrieves all versions listed on the chapter page in the given language code
def get_versions(language_id):

    page_html = shared.get_url_content(
        'https://www.bible.com/languages/{}'.format(
            language_id.replace('-', '_')))

    parser = VersionParser()
    parser.feed(page_html)

    return parser.versions
