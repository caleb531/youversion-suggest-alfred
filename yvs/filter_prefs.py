# yvs.filter_prefs

from __future__ import unicode_literals
import re
import yvs.shared as shared


PREF_RESULTS = [
    {
        'title': 'Language',
        'subtitle': 'Set your preferred language',
        'autocomplete': 'language ',
        'valid': 'no'
    },
    {
        'title': 'Version',
        'subtitle': 'Set your preferred version',
        'autocomplete': 'version ',
        'valid': 'no'
    }
]


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


# Associate preference with callback to retrieve its possible values
PREF_CALLBACKS = {
    'language': get_language_result_list,
    'version': get_version_result_list
}


def get_pref_matches(query_str):

    patt = r'^{name}{value}$'.format(
        name=r'(\w+)',
        value=r'(?:\s?(\w+))?')
    return re.search(patt, query_str, flags=re.UNICODE)


def get_result_list(query_str):

    query_str = shared.format_query_str(query_str)
    pref_matches = get_pref_matches(query_str)
    results = []

    def filter_by_pref(result):
        return result['autocomplete'].strip().startswith(query_str.lower())

    if pref_matches:

        pref_name = pref_matches.group(1)
        pref_value = pref_matches.group(2)

        if pref_name in PREF_CALLBACKS:

            results = PREF_CALLBACKS[pref_name](pref_value)

        else:

            results = filter(filter_by_pref, PREF_RESULTS)

    else:

        results = PREF_RESULTS

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
