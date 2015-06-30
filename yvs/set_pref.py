#!/usr/bin/env python

import re
import yvs.shared as shared


def get_pair(pair_str):

    pair_matches = re.search('^(\w+):(\w+)$', pair_str, flags=re.UNICODE)

    key = pair_matches.group(1)
    value = pair_matches.group(2)
    if value.isdigit():
        value = int(value)

    return (key, value)


def set_pref(key, value):

    prefs = shared.get_prefs()
    prefs[key] = value

    if key == 'language':
        bible = shared.get_bible_data(language=value)
        # Set version to default version of new language
        prefs['version'] = bible['default_version']

    shared.update_prefs(prefs)


def main(pair_str='{query}'):

    key, value = get_pair(pair_str)
    set_pref(key, value)

if __name__ == '__main__':
    main()
