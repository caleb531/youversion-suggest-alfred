#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import time
import shared


def get_result_list(query_str, prefs=None):

    # query_str = shared.format_query_str(query_str)
    # query = shared.get_query_object(query_str)
    results = []
    recent_refs = shared.get_recent_refs()

    for ref_uid in recent_refs:

        ref = shared.get_ref_object(ref_uid, prefs)
        full_ref = shared.get_full_ref(ref)
        result = {
            'uid': 'yvs-{}'.format(ref_uid),
            'arg': ref_uid,
            'title': full_ref,
            'subtitle': 'View on YouVersion',
            'valid': 'yes'
        }

    return results


def main(query_str='{query}'):

    results = get_result_list(query_str)

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
