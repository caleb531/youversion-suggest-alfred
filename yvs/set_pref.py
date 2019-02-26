#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function, unicode_literals

import json
import sys

import yvs.core as core
import yvs.cache as cache


# Parse pref set data from the given JSON string
def parse_pref_set_data(pref_set_data_str):

    pref_set_data = json.loads(pref_set_data_str)
    return pref_set_data['pref'], pref_set_data['value']


# Set the YouVersion Suggest preference with the given key
def set_pref(pref_id, value_id):

    user_prefs = core.get_user_prefs()
    user_prefs[pref_id] = value_id

    # If new language is set, ensure that preferred version is updated also
    if pref_id == 'language':
        bible = core.get_bible(language_id=value_id)
        user_prefs['version'] = bible['default_version']
        cache.clear_cache()

    core.set_user_prefs(user_prefs)


def main(pref_set_data_str):

    pref, value = parse_pref_set_data(pref_set_data_str)
    set_pref(pref['id'], value['id'])
    print('Preferred {} set to {}'.format(
        pref['name'].lower(), value['name']).encode('utf-8'))


if __name__ == '__main__':
    main(sys.argv[1].decode('utf-8'))
