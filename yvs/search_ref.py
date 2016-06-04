# yvs.search_ref
# coding=utf-8

from __future__ import unicode_literals
import sys
import urllib
import webbrowser
import yvs.shared as shared


def get_search_url(ref_uid):

    user_prefs = shared.get_user_prefs()
    search_engines = shared.get_search_engines()
    search_engine = shared.get_search_engine(
        search_engines, user_prefs['search_engine'])

    ref = shared.get_ref_object(ref_uid, user_prefs)
    full_ref = shared.get_full_ref(ref)
    encoded_ref = urllib.quote_plus(full_ref.encode('utf-8'))

    return search_engine['url'].format(query=encoded_ref)


def main(ref_uid):

    webbrowser.open(get_search_url(ref_uid))


if __name__ == '__main__':
    main(sys.argv[1].decode('utf-8'))
