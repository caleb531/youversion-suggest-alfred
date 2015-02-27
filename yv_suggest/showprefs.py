#!/usr/bin/env python

import shared


def get_language_result_list():

    prefs = shared.get_prefs()
    languages = shared.get_languages()
    results = []

    for language in languages:

        result = {
            'uid': 'yv-language-{}'.format(language['id']),
            'arg': 'language:{}'.format(language['id']),
            'title': language['name']
        }
        if language['id'] == prefs['language']:
            result['subtitle'] = 'This is already your preferred language'
            result['valid'] = 'no'
        else:
            result['subtitle'] = 'Set this as your preferred language'
        results.append(result)

    return results


def get_version_result_list():

    prefs = shared.get_prefs()
    bible = shared.get_bible_data(prefs['language'])
    results = []

    for version in bible['versions']:

        result = {
            'uid': 'yv-version-{}'.format(version['id']),
            'arg': 'version:{}'.format(version['id']),
            'title': version['name']
        }
        if version['id'] == prefs['version']:
            result['subtitle'] = 'This is already your preferred version'
            result['valid'] = 'no'
        else:
            result['subtitle'] = 'Set this as your preferred version'
        results.append(result)

    return results


def main(query_str='{query}'):

    if query_str.startswith('l'):
        results = get_language_result_list()
    elif query_str.startswith('v'):
        results = get_version_result_list()
    else:
        results = [{
            'uid': 'yv-noprefs',
            'title': 'Cannot determine preference to set',
            'subtitle': 'Please begin typing a valid preference name'
        }]

    print(shared.get_result_list_xml(results))


if __name__ == '__main__':
    main()
