import os
import shutil

import requests_mock
from tqdm import tqdm

from page_loader.download import download_url, \
    LIST_, download
from page_loader.html import find_content
from page_loader.url import create_filename_for_file

URL = 'https://www.mirf.ru/comics/saga-komiks'
PATH = os.path.join(os.getcwd(), 'tests', 'tmp')
NAME = 'mirf-ru-comics-saga-komiks.html'
FIXTURE_PATH = os.path.join(os.getcwd(), 'tests', 'fixtures')
CATALOG_NAME = 'mirf-ru-comics-saga-komiks_files'
FIXTURE_FIND_FILE = os.path.join(FIXTURE_PATH, 'fixture_find.html')
CONTENT_FIXTURE = os.path.join(FIXTURE_PATH, 'mirf-ru-comics-saga-komiks_files',
                               'mirf-ru-wp-content-plugins-push-js-push-lib.js')
URL_FOR_CONTENT = 'https://www.mirf.ru/wp-content/plugins/push/js/push.lib.js'
fixture_list = ['https://docs.python-requests.org'
                '/_static/requests-sidebar.png',
                'https://docs.python-requests.org'
                '/_static/documentation_options.js',
                'https://docs.python-requests.org'
                '/_static/jquery.js', 'https://docs.python-req'
                                      'uests.org/_static'
                                      '/underscore.js',
                'https://docs.python-requests.org'
                '/_static/doctools.js',
                'https://docs.python-requests.org'
                '/_static/pygments.css',
                'https://docs.python-requests.org'
                '/_static/alabaster.css',
                'https://docs.python-requests.org'
                '/en/latest/index.html',
                'https://docs.python-requests.org'
                '/genindex/', 'https://docs.python-'
                              'requests.org/search/',
                'https://docs.python-requests.org'
                '/user/install/',
                'https://docs.python-requests.org'
                '/_static/custom.css']


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
        download_url(URL, PATH)
        check = os.path.isfile(os.path.join(PATH, NAME))
        assert check is True


def test_page_all():
    ready()
    os.makedirs(os.path.join(PATH, CATALOG_NAME))
    filepath = os.path.join(PATH, CATALOG_NAME)
    list_ = []
    for item in LIST_:
        sample = find_content(os.path.join(os.getcwd(),
                                           'tests',
                                           'fixtures',
                                           'download_resourses.html'),
                              item, URL)
        list_ = list_ + sample
    for link in tqdm(list_):
        with requests_mock.Mocker(real_http=True) as m:
            m.get(URL)
            download_url(link, filepath)
    lenght = len(os.listdir(os.path.join(PATH, CATALOG_NAME)))
    assert lenght == 15
    check = os.path.isfile(os.path.join(PATH, CATALOG_NAME,
                                        'mirf-ru-wp-'
                                        'content-themes-mirf'
                                        '-css-delement.css'))
    assert check is True


def test_find_content():
    list_ = []
    for item in LIST_:
        sample = find_content(FIXTURE_FIND_FILE, item,
                              'https://docs.python-requests.org/')
        list_ = list_ + sample
    assert list_ == fixture_list


def test_naming():
    name = create_filename_for_file(URL)
    assert name == NAME


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
        content = f.read()
        with requests_mock.Mocker() as m:
            m.get(URL_FOR_CONTENT, text=content)
            download_url(URL_FOR_CONTENT, PATH)
            with \
                    open(os.path.join(PATH,
                                      'mirf-ru-wp-content-plugins-push'
                                      '-js-push-lib.js')) as q:
                compare = q.read()
                assert compare == content
