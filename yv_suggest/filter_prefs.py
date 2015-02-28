#!/usr/bin/env python

from __future__ import unicode_literals
import re
import shared


def get_language_result_list(query_str, ignore_prefs=True):

    prefs = shared.get_prefs(ignore_prefs)
    languages = shared.get_languages()
    results = []

    for language in languages:

        result = {
            'uid': 'yvs-language-{}'.format(language['id']),
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


def get_version_result_list(query_str, ignore_prefs=True):

    prefs = shared.get_prefs(ignore_prefs)
    versions = shared.get_versions(prefs['language'])
    results = []

    for version in versions:

        result = {
            'uid': 'yvs-version-{}'.format(version['id']),
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


def get_pref_matches(query_str):

    patt = '^{name}{value}$'.format(
        name='(\w+)',
        value='(?:\s?(\w+))?')
    return re.search(patt, query_str, flags=re.UNICODE)


def get_result_list(query_str, ignore_prefs=True):

    query_str = shared.format_query_str(query_str)
    pref_matches = get_pref_matches(query_str)
    results = []

    if pref_matches:

        pref_name = pref_matches.group(1)
        pref_value = pref_matches.group(2)

        if pref_name.startswith('l'):
            results = get_language_result_list(pref_value, ignore_prefs)
        elif pref_name.startswith('v'):
            results = get_version_result_list(pref_value, ignore_prefs)

    return results


def main(query_str='{query}', ignore_prefs=True):

    results = get_result_list(query_str, ignore_prefs)

    if not results:
        results = [{
            'uid': 'yvs-noprefs',
            'title': 'Cannot determine preference to set',
            'subtitle': 'Please enter a valid preference name',
            'valid': 'no'
        }]

    print(shared.get_result_list_xml(results))


if __name__ == '__main__':
    main(ignore_prefs=False)
