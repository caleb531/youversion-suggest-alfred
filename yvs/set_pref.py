# yvs.set_pref
# coding=utf-8

from __future__ import unicode_literals
import re
import yvs.shared as shared


# Parse key and value from the given key-value string
def get_key_value(key_value_str):

    key_value_matches = re.search(
        r'^(\w+):(\w+)$', key_value_str, flags=re.UNICODE)

    key = key_value_matches.group(1)
    value = key_value_matches.group(2)
    if value.isdigit():
        value = int(value)

    return (key, value)


# Set the YouVersion preference with the given key
def set_pref(key, value):

    user_prefs = shared.get_user_prefs()
    user_prefs[key] = value

    # If new language is set, ensure that preferred version is updated also
    if key == 'language':
        bible = shared.get_bible_data(language=value)
        user_prefs['version'] = bible['default_version']

    shared.set_user_prefs(user_prefs)


def main(key_value_str):

    key, value = get_key_value(key_value_str)
    set_pref(key, value)


if __name__ == '__main__':
    main('{query}')
