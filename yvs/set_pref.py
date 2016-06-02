# yvs.set_pref
# coding=utf-8

from __future__ import unicode_literals
import json
import yvs.shared as shared


# Parse pref set data from the given JSON string
def parse_pref_set_data(pref_set_data_str):

    pref_set_data = json.loads(pref_set_data_str)
    return pref_set_data['pref'], pref_set_data['value']


# Set the YouVersion Suggest preference with the given key
def set_pref(pref_id, value_id):

    user_prefs = shared.get_user_prefs()
    user_prefs[pref_id] = value_id

    # If new language is set, ensure that preferred version is updated also
    if pref_id == 'language':
        bible = shared.get_bible_data(language=value_id)
        user_prefs['version'] = bible['default_version']

    shared.set_user_prefs(user_prefs)


def main(pref_set_data_str):

    pref, value = parse_pref_set_data(pref_set_data_str)
    set_pref(pref['id'], value['id'])
    print('Set preferred {} to {}'.format(
        pref['name'].lower(), value['name']).encode('utf-8'))


if __name__ == '__main__':
    main('{query}')
