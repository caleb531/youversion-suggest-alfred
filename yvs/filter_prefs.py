# yvs.filter_prefs
# coding=utf-8

from __future__ import unicode_literals

import json
import re
import sys
from operator import itemgetter

import yvs.shared as shared


# Returns a list of definition objects for all available preferences
def get_pref_defs(user_prefs):

    return [
        {
            'id': 'language',
            'name': 'Language',
            'values': shared.get_languages(),
            'description': 'Set your preferred language for Bible content'
        },
        {
            'id': 'version',
            'name': 'Version',
            'values': sorted(
                shared.get_versions(user_prefs['language']),
                key=itemgetter('name')),
            'description': 'Set the default version for Bible content'
        },
        {
            'id': 'refformat',
            'name': 'Reference Format',
            'values': get_ref_format_values(user_prefs),
            'description': 'Set the default format for copied Bible '
                           'references',
            'customizable': True
        }
    ]


# Get a list of all available ref formats
def get_ref_format_values(user_prefs):

    ref = shared.get_ref(
        '111/jhn.11.35', shared.get_default_user_prefs())
    ref_formats = [
        '{name} ({version})\n\n{content}',
        '{name} {version}\n\n{content}',
        '{content}\n({name} {version})',
        '"{content}"\n{name} {version}',
        '"{content}"\n{name} {version}\n{url}'
    ]
    # Display the user's current preference in the list
    if user_prefs['refformat'] not in ref_formats:
        ref_formats.append(user_prefs['refformat'])

    return [get_ref_format_value(ref_format, ref)
            for ref_format in ref_formats]


def get_ref_format_value(ref_format, ref):

    return {
        'id': ref_format,
        'name': ref_format.format(
            name=shared.get_basic_ref_name(ref),
            version=ref['version'],
            content='Jesus wept.',
            url=shared.get_ref_url(ref['uid']))
        .replace('\n', ' ¬ ')
        # Since the above substitution adds whitespace to both sides of the
        # return symbol, the whitespace needs to be collapsed in the case of
        # consecutive return symbols
        .replace('  ', ' ')
    }


# Get the value object with the given ID for the given preference
def get_pref_value(pref_def, value_id):

    values = pref_def['values']
    for value in values:
        if value['id'] == value_id:
            return value
    return None


# Retrieves Alfred result object for this preference
def get_pref_def_result(pref_def, user_prefs):

    value = get_pref_value(pref_def, user_prefs[pref_def['id']])
    result = {}

    result['uid'] = 'yvs-{}'.format(pref_def['id'])
    result['title'] = pref_def['name']
    result['subtitle'] = pref_def['description']
    if value is not None:
        result['subtitle'] += ' (currently {})'.format(value['name'])
    result['autocomplete'] = '{} '.format(pref_def['id'].replace('_', ''))
    result['valid'] = False

    return result


# Returns True if the given query string matches the given preference name;
# otherwise, returns False
def query_matches_value_title(pref_value, query_str):
    matches = re.search(r'\b{}'.format(
        re.escape(query_str)), pref_value, flags=re.IGNORECASE)
    if matches:
        return True
    else:
        return False


# Get the result object for a single preference value
def get_value_result(value, user_prefs, pref_def):

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
        result['valid'] = False
    else:
        result['subtitle'] = 'Set this as your preferred {}'.format(
            pref_def['name'].lower())

    # Allow user to customize the values of select preferences (e.g.
    # refformat) by pressing TAB key
    if pref_def.get('customizable', False):
        result['autocomplete'] = '{key} {value}'.format(
            key=pref_def['id'],
            value=value['id'].replace('\n', '\\n'))

    return result


# Retrieves Alfred result list of all available values for this preference
def get_value_result_list(user_prefs, pref_def, query_str):

    results = [get_value_result(value, user_prefs, pref_def)
               for value in pref_def['values']
               if not query_str or query_matches_value_title(
                   value['name'], query_str)]

    if not results:
        results.append({
            'title': 'No Results',
            'subtitle': 'No values matching {}'.format(query_str),
            'valid': False
        })

    return results


# Parses a preference key and optional value from the given query string
def get_pref_matches(query_str):

    patt = r'^{key}{value}.*?$'.format(
        key=r'(\w+)',
        value=r'(?:\s?(\w+))?')
    return re.search(patt, query_str, flags=re.UNICODE)


# Simplify the given preference key for comparison with a query string
def normalize_pref_key(pref_key):

    return pref_key.replace('_', '').lower()


# Format the query string specifically for this script filter
def normalize_query_str(query_str):

    return shared.normalize_query_str(query_str.replace('_', ''))


# Retrieves result list of available preferences, filtered by the given query
def get_pref_result_list(user_prefs, pref_defs, pref_key_query_str=''):

    return [get_pref_def_result(pref_def, user_prefs) for pref_def in pref_defs
            if normalize_pref_key(pref_def['id']).startswith(
                pref_key_query_str)
            or normalize_pref_key(pref_def['name']).startswith(
                pref_key_query_str)]


# Retrieves result list of preferences or their respective values (depending on
# the given query string)
def get_result_list(query_str):

    user_prefs = shared.get_user_prefs()
    pref_defs = get_pref_defs(user_prefs)
    query_str = normalize_query_str(query_str)
    pref_matches = get_pref_matches(query_str)
    results = []

    if pref_matches:

        pref_key_query_str = pref_matches.group(1)
        pref_value_query_str = pref_matches.group(2)

        for pref_def in pref_defs:
            # If key name in query exactly matches a preference key name
            if normalize_pref_key(pref_def['id']) == pref_key_query_str:
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
            'valid': False
        })

    print(shared.get_result_list_feedback_str(results))


if __name__ == '__main__':
    main(sys.argv[1].decode('utf-8'))
