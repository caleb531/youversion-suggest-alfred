# yvs.get_ref_id
# coding=utf-8
from __future__ import print_function
import sys


# Parse reference identifier from copied reference content for output
print(sys.argv[1].split('\n', 1)[0].rstrip(), end='')
