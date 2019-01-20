# yvs.set_pref
# coding=utf-8

from __future__ import unicode_literals

import json
import sys

import yvs.shared as shared


# Parse pref set data from the given JSON string
def parse_pref_set_data_str(pref_set_data_str):

    pref_set_data = json.loads(
        pref_set_data_str)['alfredworkflow']['variables']
    return [pref_set_data[key] for key in
            ('pref_id', 'pref_name', 'value_id', 'value_name')]


# Set the YouVersion Suggest preference with the given key
def set_pref(pref_id, value_id):

    user_prefs = shared.get_user_prefs()
    user_prefs[pref_id] = value_id

    # If new language is set, ensure that preferred version is updated also
    if pref_id == 'language':
        bible = shared.get_bible_data(language_id=value_id)
        user_prefs['version'] = bible['default_version']
        shared.clear_cache()

    shared.set_user_prefs(user_prefs)


def main(pref_set_data_str):

    pref_id, pref_name, value_id, value_name = parse_pref_set_data_str(
        pref_set_data_str)
    set_pref(pref_id, value_id)
    print(pref_set_data_str.encode('utf-8'))


if __name__ == '__main__':
    main(sys.argv[1].decode('utf-8'))
