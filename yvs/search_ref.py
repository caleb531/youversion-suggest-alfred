# yvs.search_ref

import urllib
import webbrowser
import yvs.shared as shared


def get_search_url(ref_uid):

    prefs = shared.get_prefs()
    search_engines = shared.get_search_engines()
    search_engine = shared.get_search_engine(
        search_engines, prefs['search_engine'])

    ref = shared.get_ref_object(ref_uid, prefs)
    full_ref = shared.get_full_ref(ref)
    encoded_ref = urllib.quote_plus(full_ref.encode('utf-8'))

    return search_engine['url'].format(query=encoded_ref)


def main(ref_uid):

    webbrowser.open(get_search_url(ref_uid))


if __name__ == '__main__':
    main('{query}')
