# yvs.filter_prefs
# coding=utf-8

from __future__ import unicode_literals
import json
import re
import sys
import yvs.shared as shared


# Returns a list of definition objects for all available preferences
def get_pref_defs(user_prefs):

    return [
        {
            'id': 'language',
            'name': 'Language',
            'values': shared.get_languages()
        },
        {
            'id': 'version',
            'name': 'Version',
            'values': shared.get_versions(user_prefs['language'])
        }
    ]


# Get the value object with the given ID for the given preference
def get_pref_value(pref_def, value_id):

    values = pref_def['values']
    for value in values:
        if value['id'] == value_id:
            return value
    return None


# Retrieves Alfred result object for this preference
def get_pref_result(pref_def, user_prefs):

    value = get_pref_value(pref_def, user_prefs[pref_def['id']])
    result = {}

    result['uid'] = 'yvs-{}'.format(pref_def['id'])
    result['title'] = pref_def['name']
    result['subtitle'] = 'Set your preferred {}'.format(
        pref_def['name'].lower())
    if value is not None:
        result['subtitle'] += ' (currently {})'.format(value['name'])
    result['autocomplete'] = '{} '.format(pref_def['id'].replace('_', ''))
    result['valid'] = 'no'

    return result


# Retrieves Alfred result list of all available values for this preference
def get_value_result_list(user_prefs, pref_def, query_str):

    values = pref_def['values']
    results = []

    for value in values:

        result = {
            'uid': 'yvs-{}-{}'.format(pref_def['id'], value['id']),
            'arg': json.dumps({
                'pref': {
                    'id': pref_def['id'],
                    'name': pref_def['name']
                },
                'value': {
                    'id': value['id'],
                    'name': value['name']
                }
            }),
            'title': value['name']
        }

        if value['id'] == user_prefs[pref_def['id']]:
            # If this value is the current value, indicate such
            result['subtitle'] = 'This is already your preferred {}'.format(
                pref_def['name'].lower())
            result['valid'] = 'no'
        else:
            result['subtitle'] = 'Set this as your preferred {}'.format(
                pref_def['name'].lower())

        # Show all results if query string is empty
        # Otherwise, only show results whose titles begin with query
        if not query_str or result['title'].lower().startswith(query_str):
            results.append(result)

    if not results:
        results.append({
            'title': 'No Results',
            'subtitle': 'No values matching {}'.format(query_str),
            'valid': 'no'
        })

    return results


# Parses a preference key and optional value from the given query string
def get_pref_matches(query_str):

    patt = r'^{key}{value}.*?$'.format(
        key=r'(\w+)',
        value=r'(?:\s?(\w+))?')
    return re.search(patt, query_str, flags=re.UNICODE)


# Simplify the given preference key for comparison with a query string
def format_pref_key(pref_key):

    return pref_key.replace('_', '').lower()


# Format the query string specifically for this script filter
def format_query_str(query_str):

    return shared.format_query_str(query_str.replace('_', ''))


# Retrieves result list of available preferences, filtered by the given query
def get_pref_result_list(user_prefs, pref_defs, pref_key_query_str=''):

    return [get_pref_result(pref_def, user_prefs) for pref_def in
            pref_defs if format_pref_key(pref_def['id']).startswith(
                pref_key_query_str)]


# Retrieves result list of preferences or their respective values (depending on
# the given query string)
def get_result_list(query_str):

    user_prefs = shared.get_user_prefs()
    pref_defs = get_pref_defs(user_prefs)
    query_str = format_query_str(query_str)
    pref_matches = get_pref_matches(query_str)
    results = []

    if pref_matches:

        pref_key_query_str = pref_matches.group(1)
        pref_value_query_str = pref_matches.group(2)

        for pref_def in pref_defs:
            # If key name in query exactly matches a preference key name
            if format_pref_key(pref_def['id']) == pref_key_query_str:
                # Get list of available values for the given preference
                results = get_value_result_list(
                    user_prefs, pref_def, pref_value_query_str)
                break
        # If no exact matches, filter list of available preferences by query
        if not results:
            results = get_pref_result_list(
                user_prefs, pref_defs, pref_key_query_str)

    else:

        # Should show all available preferences if query is empty
        # or if query does not match
        results = get_pref_result_list(user_prefs, pref_defs)

    return results


def main(query_str):

    results = get_result_list(query_str)
    if not results:
        results.append({
            'title': 'No Results',
            'subtitle': 'No preferences matching \'{}\''.format(query_str),
            'valid': 'no'
        })

    print(shared.get_result_list_feedback_str(results))


if __name__ == '__main__':
    main(sys.argv[1].decode('utf-8'))
