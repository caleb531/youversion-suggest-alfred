#!/usr/bin/env python
# Open Google search for Bible reference

import webbrowser
import urllib
import re
import shared

base_url = 'https://www.google.com/search'


ref_uid_patt = '{version}/{book_id}\.{chapter}(?:\.{verses})?'.format(
    version='([a-z]+\d*)',
    book_id='(\d?[a-z]+)',
    chapter='(\d+)',
    verses='(\d+(?:-\d+)?)')


def get_full_ref(ref_uid):
    ref_uid_matches = re.match(ref_uid_patt, ref_uid)
    book_match = ref_uid_matches.group(2)
    chapter_match = ref_uid_matches.group(3)
    bible = shared.get_bible_data()
    for book in bible['books']:
        if book['id'] == book_match:
            book_name = book['name']
            break
    ref = '{book} {chapter}'.format(
        book=book_name,
        chapter=chapter_match)
    verses_match = ref_uid_matches.group(4)
    if verses_match:
        ref += ":{verses}".format(verses=verses_match)
    version_match = ref_uid_matches.group(1).upper()
    ref += " ({version})".format(version=version_match)
    return ref


def get_search_url(ref_uid):
    ref = get_full_ref(ref_uid)
    encoded_ref = urllib.quote_plus(ref)
    return '{base}?q={query_str}'.format(base=base_url, query_str=encoded_ref)


def open_search_url(ref_uid):
    webbrowser.open(get_search_url(ref_uid))


def main(ref_uid='{query}'):
    open_search_url(ref_uid)

if __name__ == '__main__':
    main()
