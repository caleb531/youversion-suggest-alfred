# yvs.filter_prefs

from __future__ import unicode_literals
import re
import yvs.shared as shared
from functools import partial
from operator import itemgetter


# Returns a list of definition objects for all available preferences
def get_pref_defs(user_prefs):

    return [
        {
            'key': 'language',
            'name': 'language',
            'title': 'Language',
            'values': shared.get_languages
        },
        {
            'key': 'version',
            'name': 'version',
            'title': 'Version',
            'values': partial(shared.get_versions, user_prefs['language'])
        },
        {
            'key': 'searchEngine',
            'name': 'search engine',
            'title': 'Search Engine',
            'values': shared.get_search_engines
        }
    ]


# Retrieves Alfred result object for this preference
def get_pref_result(pref):

    return {
        'title': pref['title'],
        'subtitle': 'Set your preferred \'{}\''.format(pref['name']),
        'autocomplete': '{} '.format(pref['key']),
        'valid': 'no'
    }


# Retrieves Alfred result list of all available values for this preference
def get_value_result_list(user_prefs, pref, query_str):

    values = pref['values']()
    results = []

    for value in values:

        result = {
            'arg': '{}:{}'.format(pref['key'], value['id']),
            'title': value['name']
        }

        if value['id'] == user_prefs[pref['key']]:
            # If this value is the current value, indicate such
            result['subtitle'] = ('This is already your preferred {}'
                                  .format(pref['name']))
            result['valid'] = 'no'
        else:
            result['subtitle'] = 'Set this as your preferred {}'.format(
                pref['name'])

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


# Retrieves result list of available preferences, filtered by the given query
def get_pref_result_list(query_str, prefs):

    return [get_pref_result(pref) for pref in
            prefs if pref['key'].lower().startswith(query_str)]


# Retrieves result list of preferences or their respective values (depending on
# the given query string)
def get_result_list(query_str):

    user_prefs = shared.get_user_prefs()
    pref_defs = get_pref_defs(user_prefs)
    query_str = shared.format_query_str(query_str)
    pref_matches = get_pref_matches(query_str)
    results = []

    if pref_matches:

        pref_key = pref_matches.group(1)
        pref_value = pref_matches.group(2)

        for pref_def in pref_defs:
            # If key name in query exactly matches a preference key name
            if pref_def['key'].lower() == pref_key:
                # Get list of available values for the given preference
                results = get_value_result_list(
                    user_prefs, pref_def, pref_value)
                break
        # If no exact matches, filter list of available preferences by query
        if not results:
            results = get_pref_result_list(query_str, pref_defs)

    else:

        # Should show all available preferences if query is empty
        # or if query does not match
        results = get_pref_result_list(query_str, pref_defs)

    # Always sort results by title in this case
    results.sort(key=itemgetter('title'))

    return results


def main(query_str):

    results = get_result_list(query_str)
    if not results:
        results.append({
            'title': 'No Results',
            'subtitle': 'No preferences matching \'{}\''.format(query_str),
            'valid': 'no'
        })

    print(shared.get_result_list_xml(results))


if __name__ == '__main__':
    main('{query}')
