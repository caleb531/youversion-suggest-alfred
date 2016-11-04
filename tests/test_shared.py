# tests.test_shared

from __future__ import unicode_literals
import tests
import yvs.shared as yvs
import nose.tools as nose
from mock import Mock, NonCallableMock, patch

with open('tests/html/psa.23.html') as html_file:
    patch_urlopen = patch(
        'urllib2.urlopen', return_value=NonCallableMock(
            read=Mock(return_value=html_file.read())))


def set_up():
    patch_urlopen.start()
    tests.set_up()


def tear_down():
    patch_urlopen.stop()
    tests.tear_down()


@nose.with_setup(set_up, tear_down)
@patch('urllib2.Request')
def test_get_url_content(request):
    """should fetch uncompressed URL content"""
    url = 'https://www.bible.com/bible/59/psa.23'
    yvs.get_url_content(url)
    request.assert_called_once_with(url, headers={
        'User-Agent': 'YouVersion Suggest',
        'Accept-Encoding': 'gzip, deflate'
    })
