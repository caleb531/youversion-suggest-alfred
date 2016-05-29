# yvs.view_ref
# coding=utf-8

from __future__ import unicode_literals
import webbrowser
import yvs.shared as shared


def open_ref_url(ref_uid):
    webbrowser.open(shared.get_ref_url(ref_uid))


def main(ref_uid):
    open_ref_url(ref_uid)


if __name__ == '__main__':
    main('{query}')
