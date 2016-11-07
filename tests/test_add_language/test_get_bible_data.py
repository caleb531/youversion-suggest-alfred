# tests.test_add_language.test_update_language_list

from __future__ import unicode_literals

import nose.tools as nose
from mock import patch

# import yvs.shared as yvs
import utilities.add_language as add_lang
from tests.test_add_language import set_up, tear_down

VERSIONS = [
    {'id': 123, 'name': 'ABC'},
    {'id': 234, 'name': 'DEF'},
    {'id': 345, 'name': 'GHI'},
    {'id': 456, 'name': 'JKL'}
]
BOOKS = [
    {'id': 'gen', 'name': 'Genesis'},
    {'id': '1sa', 'name': '1 Samuel'},
    {'id': 'jhn', 'name': 'John'}
]


@nose.with_setup(set_up, tear_down)
@patch('utilities.add_language.get_books', return_value=BOOKS)
@patch('utilities.add_language.get_versions', return_value=VERSIONS)
def test_get_bible_data_default_version(get_versions, get_books):
    language_id = 'spa'
    default_version = 345
    bible = add_lang.get_bible_data(language_id, default_version)
    get_versions.assert_called_once_with(
        language_id=language_id, max_version_id=None)
    nose.assert_equal(bible['default_version'], default_version)
