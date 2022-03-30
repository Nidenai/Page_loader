import os
import shutil

import requests_mock
from bs4 import BeautifulSoup as bs

from page_loader.download import download_url, \
    download, save_file
from page_loader.html import prepare
from page_loader.url import create_filename_for_file, create_link

URL = 'https://www.mirf.ru/comics/saga-komiks'
PATH = os.path.join(os.getcwd(), 'tests', 'tmp')
NAME = 'mirf-ru-comics-saga-komiks.html'
FIXTURE_PATH = os.path.join(os.getcwd(), 'tests', 'fixtures')
CATALOG_NAME = 'mirf-ru-comics-saga-komiks_files'
FIXTURE_FIND_FILE = os.path.join(FIXTURE_PATH, 'fixture_find.html')
RESOURSE_FILE = os.path.join(PATH, 'file_to_compare.html')
CONTENT_FIXTURE = os.path.join(FIXTURE_PATH, 'mirf-ru-comics-sa'
                                             'ga-komiks_files',
                               'mirf-ru-wp-content-plugins-p'
                               'ush-js-push-lib.js')
URL_FOR_CONTENT = 'https://www.mirf.ru/wp-content/plugins/push/js/push.lib.js'
URL_FOR_URLTEST = 'https://www.mirf.ru'
ARG_FOR_URLTEST = 'src'
TAG_FOR_URLTEST = bs('<img alt="" src="https://www.mirf.'
                     'ru/wp-content/uploads/2021/10/Shape'
                     '.svg" style="height:18px;"/>',
                     'html.parser').img
CORRECT_ANSWER = 'https://www.mirf.ru/wp-content/uploads/2021/10/Shape.svg'


def ready():
    if os.path.isfile(os.path.join(PATH, NAME)):
        os.remove(os.path.join(PATH, NAME))
    if os.path.isdir(os.path.join(PATH, CATALOG_NAME)):
        shutil.rmtree((os.path.join(PATH, CATALOG_NAME)))


def test_page_download():
    ready()
    os.makedirs(os.path.join(PATH, CATALOG_NAME))
    with requests_mock.Mocker(real_http=True) as m:
        m.get(URL)
        content = download_url(URL)
        save_file(content, PATH, url=URL)
        check = os.path.isfile(os.path.join(PATH, NAME))
        assert check is True


def test_html():
    url = 'https://docs.python-requests.org/'
    with open(FIXTURE_FIND_FILE) as r:
        content = r.read()
        with requests_mock.Mocker() as m:
            m.get(url, text=content)
            sample = prepare(RESOURSE_FILE,
                             url,
                             PATH)
            with open(os.path.join(os.getcwd(),
                                   'tests',
                                   'fixtures',
                                   'resourses.txt')) as q:
                fixture_list = q.read()
    assert str(sample) == fixture_list


def test_url():
    name = create_filename_for_file(URL)
    assert name == NAME
    link = create_link(URL_FOR_URLTEST, TAG_FOR_URLTEST, ARG_FOR_URLTEST)
    assert link == CORRECT_ANSWER


def test_download():
    ready()
    with open(os.path.join(FIXTURE_PATH, NAME)) as f:
        content = f.read()
        with requests_mock.Mocker() as m:
            m.get(URL, text=content)
            download(URL, PATH)
            check = os.path.isfile(os.path.join(PATH, NAME))
            assert check is True
            check_folder = os.path.isdir(os.path.join(PATH, CATALOG_NAME))
            assert check_folder is True


def test_resourse():
    with open(CONTENT_FIXTURE) as f:
        fixture = f.read()
        with requests_mock.Mocker() as m:
            m.get(URL_FOR_CONTENT, text=fixture)
            content = download_url(URL_FOR_CONTENT)
            save_file(content, PATH, url=URL_FOR_CONTENT)
            with \
                    open(os.path.join(PATH,
                                      'mirf-ru-wp-content-plugins-push'
                                      '-js-push-lib.js')) as q:
                compare = q.read()
                assert compare == fixture
