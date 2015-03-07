#!/usr/bin/env python

from __future__ import unicode_literals
import re
import shared


def get_pair_matches(key_value_str):

    patt = '^{key}:{value}$'.format(
        key='(\w+)',
        value='(\w+)')

    return re.search(patt, key_value_str, flags=re.UNICODE)


def get_pair(key_value_str):

    pair_matches = get_pair_matches(key_value_str)

    key = pair_matches.group(1)
    value = pair_matches.group(2)
    if value.isdigit():
        value = int(value)

    return (key, value)


def set_pref(key, value):

    prefs = shared.get_prefs()
    prefs[key] = value

    if key == 'language':
        shared.delete_recent_refs()
        bible = shared.get_bible_data(language=value)
        # Set version to default version of new language
        prefs['version'] = bible['default_version']

    shared.update_prefs(prefs)


def main(key_value_str='{query}'):

    key, value = get_pair(key_value_str)
    set_pref(key, value)

if __name__ == '__main__':
    main()
