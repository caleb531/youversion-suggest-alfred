# yvs.search_ref

import urllib
import webbrowser
import yvs.shared as shared


base_url = 'https://www.google.com/search'


def get_search_url(ref_uid):
    ref = shared.get_ref_object(ref_uid)
    full_ref = shared.get_full_ref(ref)
    encoded_ref = urllib.quote_plus(full_ref.encode('utf-8'))
    return '{base}?q={query_str}'.format(base=base_url, query_str=encoded_ref)


def open_search_url(ref_uid):
    webbrowser.open(get_search_url(ref_uid))


def main(ref_uid):
    open_search_url(ref_uid)

if __name__ == '__main__':
    main('{query}')
