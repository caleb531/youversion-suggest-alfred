# yvs.filter_prefs

from __future__ import unicode_literals
import re
import yvs.shared as shared
from functools import partial
from operator import itemgetter


prefs = shared.get_prefs()


class Preference(object):

    def __init__(self, key, name, title, values):
        # Store key name, result name and result title for this preference
        self.key = key
        self.title = title
        self.name = name
        # Also store reference to list of accepted values
        # or function that will produce such a list
        self.values = values

    # Retrieve Alfred result object for this preference
    def get_pref_result(self):
        return {
            'title': self.title,
            'subtitle': 'Set your preferred {}'.format(self.title.lower()),
            'autocomplete': '{} '.format(self.key),
            'valid': 'no'
        }

    # Retrieve list of accepted values for this preference
    def get_values(self):
        if hasattr(self.values, '__call__'):
            return self.values()
        else:
            return self.values

    # Retrieve list of all available languages
    def get_value_result_list(self, query_str):

        values = self.get_values()
        results = []

        for value in values:

            result = {
                'arg': '{}:{}'.format(self.key, value['id']),
                'title': value['name']
            }
            if value['id'] == prefs[self.key]:
                result['subtitle'] = ('This is already your preferred {}'
                                      .format(self.name))
                result['valid'] = 'no'
            else:
                result['subtitle'] = 'Set this as your preferred value'

            if not query_str or result['title'].lower().startswith(query_str):
                results.append(result)

        if results == []:
            results.append({
                'title': 'No Results for {}'.format(self.title),
                'subtitle': ('Could not find a {} value matching the query'
                             .format(self.name)),
                'valid': 'no'
            })

        return results


# Delineate all available workflow preferences
PREFERENCES = [
    Preference(
        key='language', name='language', title='Language',
        values=shared.get_languages),
    Preference(
        key='version', name='version', title='Version',
        values=partial(shared.get_versions, prefs['language'])),
    Preference(
        key='searchEngine', name='search engine', title='Search Engine',
        values=shared.get_search_engines)
]


def get_pref_matches(query_str):

    patt = r'^{key}{value}$'.format(
        key=r'(\w+)',
        value=r'(?:\s?(\w+))?')
    return re.search(patt, query_str, flags=re.UNICODE)


# Retrieve result list of available preferences, filtered by the given query
def get_pref_result_list(query_str):

    return [pref.get_pref_result() for pref in
            PREFERENCES if pref.key.startswith(query_str)]


def get_result_list(query_str):

    query_str = shared.format_query_str(query_str)
    pref_matches = get_pref_matches(query_str)
    results = []

    if pref_matches:

        pref_key = pref_matches.group(1)
        pref_value = pref_matches.group(2)

        for pref in PREFERENCES:
            if pref.key.lower() == pref_key:
                # Get list of available values for the given preference
                results = pref.get_value_result_list(pref_value)
                break
        if not results:
            results = get_pref_result_list(query_str)

    else:

        results = get_pref_result_list(query_str)

    # Always sort results by title in this case
    results.sort(key=itemgetter('title'))

    return results


def main(query_str):

    results = get_result_list(query_str)

    if not results:
        results = [{
            'uid': 'yvs-noprefs',
            'title': 'Invalid preference name or value',
            'subtitle': 'Please enter a valid name or value to set',
            'valid': 'no'
        }]

    print(shared.get_result_list_xml(results))


if __name__ == '__main__':
    main('{query}')
