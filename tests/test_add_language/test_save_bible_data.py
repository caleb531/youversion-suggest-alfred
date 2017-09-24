# tests.test_add_language.test_save_bible_data
# coding=utf-8

from __future__ import unicode_literals
import copy
import json
import os
import os.path

import nose.tools as nose

import yvs.shared as yvs
import utilities.add_language as add_lang
from tests.test_add_language import set_up, tear_down

LANGUAGE_ID = 'swe'
BIBLE = {
    'books': [{'id': 'gen', 'name': 'Första Moseboken'}],
    'default_version': 33,
    'versions': [{'id': 33, 'name': 'BSV'}, {'id': 154, 'name': 'B2000'}]
}


@nose.with_setup(set_up, tear_down)
def test_save_bible_data_new():
    """should save Bible data to new data file if it doesn't exist"""
    bible_file_path = os.path.join(
        yvs.PACKAGED_DATA_DIR_PATH, 'languages',
        'language-{}.json'.format(LANGUAGE_ID))
    add_lang.save_bible_data(language_id=LANGUAGE_ID, bible=BIBLE)
    nose.assert_true(os.path.exists(bible_file_path))
    with open(bible_file_path, 'r') as bible_file:
        saved_bible = json.load(bible_file)
        nose.assert_equal(saved_bible, BIBLE)


@nose.with_setup(set_up, tear_down)
def test_save_bible_data_existing():
    """should update Bible data in existing data file"""
    bible_file_path = os.path.join(
        yvs.PACKAGED_DATA_DIR_PATH, 'languages',
        'language-{}.json'.format(LANGUAGE_ID))
    with open(bible_file_path, 'w') as bible_file:
        json.dump(BIBLE, bible_file)
    new_bible = copy.deepcopy(BIBLE)
    new_bible['default_version'] = 154
    add_lang.save_bible_data(language_id=LANGUAGE_ID, bible=new_bible)
    nose.assert_true(os.path.exists(bible_file_path))
    with open(bible_file_path, 'r') as bible_file:
        saved_bible = json.load(bible_file)
        nose.assert_equal(saved_bible, new_bible)
