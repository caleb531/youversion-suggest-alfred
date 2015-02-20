#!/usr/bin/env python
# Open Bible reference on YouVersion website

import webbrowser
import shared

base_url = 'https://www.bible.com/bible'


def get_ref_url(ref_uid):
    return '{base}/{uid}'.format(base=base_url, uid=ref_uid)


def open_ref_url(ref_uid):
    webbrowser.open(get_ref_url(ref_uid))


def main(ref_uid='{query}'):
    open_ref_url(ref_uid)

if __name__ == '__main__':
    main()