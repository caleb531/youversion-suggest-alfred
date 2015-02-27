#!/usr/bin/env python

import shared


def main(query_str='{query}'):

    pair = query_str.split(':')
    key, value = pair
    if value.isdigit():
        value = int(value)

    prefs = shared.get_prefs()
    prefs[key] = value

    if key == 'language':
        bible = shared.get_bible_data(value)
        # If preferred version is not in the new chosen language
        if not shared.get_version(bible['versions'], prefs['version']):
            # Set version to default version of new language
            prefs['version'] = bible['default_version']

    shared.update_prefs(prefs)

if __name__ == '__main__':
    main()
