# test_update_language_list

from __future__ import unicode_literals

import json
import os
import os.path

import nose.tools as nose

import yvs.shared as yvs
import utilities.add_language as add_lang
from tests.test_add_language import set_up, tear_down
from tests.test_add_language.decorators import redirect_stdout


@nose.with_setup(set_up, tear_down)
@redirect_stdout
def test_update_languge_list_add(out):
    """should add new languages to language list"""
    add_lang.update_language_list('kln', 'Klingon')
    langs_path = os.path.join(yvs.PACKAGED_DATA_DIR_PATH, 'languages.json')
    with open(langs_path, 'r') as langs_file:
        langs = json.load(langs_file)
        klingon_lang = None
        for lang in langs:
            if lang['id'] == 'kln':
                klingon_lang = lang
        nose.assert_is_not_none(klingon_lang)
        nose.assert_equal(klingon_lang['name'], 'Klingon')
