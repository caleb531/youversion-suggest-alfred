# yvs.get_ref_id
# coding=utf-8

from __future__ import print_function, unicode_literals

import sys


def main(ref_content):
    print(ref_content.split('\n', 1)[0].rstrip().encode('utf-8'),
          end=''.encode('utf-8'))


if __name__ == '__main__':
    main(sys.argv[1].decode('utf-8'))
