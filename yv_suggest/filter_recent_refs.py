#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import time
import shared


def query_matches_ref(query, ref):

    for i in xrange(len(query['book']), 0, -1):
        book_name = ref['book'].lower()
        if (book_name.startswith(query['book'][:i]) or
            (book_name[0].isnumeric() and
                book_name[2:].startswith(query['book'][:i]))):
            return True

    return False


def get_result_list(query_str, prefs=None):

    # query_str = shared.format_query_str(query_str)
    query = shared.get_query_object(query_str)
    results = []
    recent_refs = shared.get_recent_refs()

    for ref_uid in recent_refs:

        ref = shared.get_ref_object(ref_uid, prefs)
        if not query_str or query_matches_ref(query, ref):
            full_ref = shared.get_full_ref(ref)
            result = {
                'uid': 'yvs-{}-{}'.format(ref_uid, time.time()),
                'arg': ref_uid,
                'title': full_ref,
                'subtitle': 'View on YouVersion',
                'valid': 'yes'
            }
            results.append(result)

    return results


def main(query_str='{query}', prefs=None):

    results = get_result_list(query_str, prefs)

    if not results:
        results = [{
            'uid': 'yvs-norecent',
            'title': 'No Recent References',
            'subtitle': 'No recent references matching \'{}\''
            .format(query_str),
            'valid': 'no'
        }]

    print(shared.get_result_list_xml(results))


if __name__ == '__main__':
    main()
