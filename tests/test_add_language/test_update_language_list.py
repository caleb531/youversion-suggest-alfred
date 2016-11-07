# test_update_language_list

from __future__ import unicode_literals

import json
import os
import os.path

import nose.tools as nose

import yvs.shared as yvs
import utilities.add_language as add_lang
from tests.test_add_language import set_up, tear_down


@nose.with_setup(set_up, tear_down)
def test_update_languge_list_add():
    """should add new languages to language list"""
    kln_language_id = 'kln'
    kln_language_name = 'Klingon'
    add_lang.update_language_list(kln_language_id, kln_language_name)
    langs_path = os.path.join(yvs.PACKAGED_DATA_DIR_PATH, 'languages.json')
    with open(langs_path, 'r') as langs_file:
        langs = json.load(langs_file)
        kln_lang = None
        for lang in langs:
            if lang['id'] == kln_language_id:
                kln_lang = lang
        nose.assert_is_not_none(kln_lang)
        nose.assert_equal(kln_lang['name'], kln_language_name)
