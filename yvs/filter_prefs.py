# yvs.filter_prefs

from __future__ import unicode_literals
import re
import yvs.shared as shared
from operator import itemgetter


class Preference(object):

    def __init__(self, name, title, get_value_result_list):
        # Store key name and result title for this preference
        self.name = name
        self.title = title
        # Also store reference to function that produces a result list of
        # possible values for this preference
        self.get_value_result_list = get_value_result_list

    # Retrieve Alfred result object for this preference
    def get_pref_result(self):
        return {
            'title': self.title,
            'subtitle': 'Set your preferred {}'.format(self.title.lower()),
            'autocomplete': '{} '.format(self.name),
            'valid': 'no'
        }


# Retrieve list of all available languages
def get_language_result_list(query_str):

    prefs = shared.get_prefs()
    languages = shared.get_languages()
    results = []

    for language in languages:

        result = {
            'arg': 'language:{}'.format(language['id']),
            'title': language['name']
        }
        if language['id'] == prefs['language']:
            result['subtitle'] = 'This is already your preferred language'
            result['valid'] = 'no'
        else:
            result['subtitle'] = 'Set this as your preferred language'

        if not query_str or result['title'].lower().startswith(query_str):
            results.append(result)

    return results


# Retrieve list of all available versions for the current preferred language
def get_version_result_list(query_str):

    prefs = shared.get_prefs()
    versions = shared.get_versions(prefs['language'])
    results = []

    for version in versions:

        result = {
            'arg': 'version:{}'.format(version['id']),
            'title': version['name']
        }
        if version['id'] == prefs['version']:
            result['subtitle'] = 'This is already your preferred version'
            result['valid'] = 'no'
        else:
            result['subtitle'] = 'Set this as your preferred version'

        if not query_str or result['title'].lower().startswith(query_str):
            results.append(result)

    return results


# Delineate all available workflow preferences
PREFERENCES = {
    'language': Preference(
        name='language', title='Language',
        get_value_result_list=get_language_result_list),
    'version': Preference(
        name='version', title='Version',
        get_value_result_list=get_version_result_list)
}


def get_pref_matches(query_str):

    patt = r'^{name}{value}$'.format(
        name=r'(\w+)',
        value=r'(?:\s?(\w+))?')
    return re.search(patt, query_str, flags=re.UNICODE)


# Retrieve result list of available preferences, filtered by the given query
def get_pref_result_list(query_str):

    return [pref.get_pref_result() for pref_name, pref in
            PREFERENCES.iteritems() if pref_name.startswith(query_str)]


def get_result_list(query_str):

    query_str = shared.format_query_str(query_str)
    pref_matches = get_pref_matches(query_str)
    results = []

    if pref_matches:

        pref_name = pref_matches.group(1)
        pref_value = pref_matches.group(2)

        if pref_name in PREFERENCES:
            # Get list of available values for the given preference
            results = PREFERENCES[pref_name].get_value_result_list(pref_value)
        else:
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

    print shared.get_result_list_xml(results)


if __name__ == '__main__':
    main('{query}')
