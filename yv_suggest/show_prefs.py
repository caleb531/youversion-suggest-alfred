#!/usr/bin/env python

from __future__ import unicode_literals
import re
import shared


def get_languages():

    languages_path = os.path.join(get_package_path(), 'data', 'languages.json')
    with open(languages_path, 'r') as languages_file:
        languages = json.load(languages_file)

    return languages


def get_language_result_list(query_str):

    prefs = shared.get_prefs()
    languages = get_languages()
    results = []

    for language in languages:

        result = {
            'uid': 'yv-language-{}'.format(language['id']),
            'arg': 'language:{}'.format(language['id']),
            'title': language['name']
        }
        if language['id'] == prefs['language']:
            result['subtitle'] = ('{} is already your preferred language'
                                  .format(result['title']))
            result['valid'] = 'no'
        else:
            result['subtitle'] = 'Set this as your preferred language'

        if not query_str or result['title'].startswith(query_str):
            results.append(result)

    return results


def get_version_result_list(query_str):

    prefs = shared.get_prefs()
    versions = shared.get_bible_data(prefs['language'])['versions']
    results = []

    for version in versions:

        result = {
            'uid': 'yv-version-{}'.format(version['id']),
            'arg': 'version:{}'.format(version['id']),
            'title': version['name']
        }
        if version['id'] == prefs['version']:
            result['subtitle'] = ('{} is already your preferred version'
                                  .format(result['title']))
            result['valid'] = 'no'
        else:
            result['subtitle'] = 'Set {} as your preferred version'.format(
                result['title'])

        if not query_str or result['title'].lower().startswith(query_str):
            results.append(result)

    return results


def get_pref_matches(query_str):

    patt = '^{name}{value}$'.format(
        name='(\w+)',
        value='(?:\s?(\w+))?')
    return re.search(patt, query_str, flags=re.UNICODE)


def get_result_list(query_str):

    query_str = shared.format_query_str(query_str)
    pref_matches = get_pref_matches(query_str)
    results = []

    if pref_matches:

        pref_name = pref_matches.group(1)
        pref_value = pref_matches.group(2)

        if pref_name:
            if pref_name.startswith('l'):
                results = get_language_result_list(pref_value)
            elif pref_name.startswith('v'):
                results = get_version_result_list(pref_value)

    return results


def main(query_str='{query}'):

    results = get_result_list(query_str)

    print(shared.get_result_list_xml(results))


if __name__ == '__main__':
    main()
