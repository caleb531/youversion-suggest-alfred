#!/usr/bin/env python

import urllib
import webbrowser
import shared


base_url = 'https://www.google.com/search'


def get_search_url(ref_uid, prefs=None):
    ref = shared.get_ref_object(ref_uid, prefs)
    full_ref = shared.get_full_ref(ref)
    encoded_ref = urllib.quote_plus(full_ref)
    return '{base}?q={query_str}'.format(base=base_url, query_str=encoded_ref)


def open_search_url(ref_uid, prefs=None):
    webbrowser.open(get_search_url(ref_uid, prefs))


def main(ref_uid, prefs=None):
    open_search_url(ref_uid, prefs)

if __name__ == '__main__':
    main('{query}')
