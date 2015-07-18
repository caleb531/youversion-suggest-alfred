# yvs.view_ref

import webbrowser

BASE_URL = 'https://www.bible.com/bible'


def get_ref_url(ref_uid):
    return '{base}/{uid}'.format(base=BASE_URL, uid=ref_uid)


def open_ref_url(ref_uid):
    webbrowser.open(get_ref_url(ref_uid))


def main(ref_uid):
    open_ref_url(ref_uid)

if __name__ == '__main__':
    main('{query}')
