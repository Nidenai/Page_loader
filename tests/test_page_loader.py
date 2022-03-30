import os
import shutil

import requests_mock
from tqdm import tqdm

from page_loader.download import download_url, \
    download, save_file
from page_loader.html import prepare
from page_loader.url import create_filename_for_file

URL = 'https://www.mirf.ru/comics/saga-komiks'
PATH = os.path.join(os.getcwd(), 'tests', 'tmp')
NAME = 'mirf-ru-comics-saga-komiks.html'
FIXTURE_PATH = os.path.join(os.getcwd(), 'tests', 'fixtures')
CATALOG_NAME = 'mirf-ru-comics-saga-komiks_files'
FIXTURE_FIND_FILE = os.path.join(FIXTURE_PATH, 'fixture_find.html')
CONTENT_FIXTURE = os.path.join(FIXTURE_PATH, 'mirf-ru-comics-sa'
                                             'ga-komiks_files',
                               'mirf-ru-wp-content-plugins-p'
                               'ush-js-push-lib.js')
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
        content = download_url(URL)
        save_file(content, PATH, url=URL)
        check = os.path.isfile(os.path.join(PATH, NAME))
        assert check is True


def astest_page_all():
    ready()
    os.makedirs(os.path.join(PATH, CATALOG_NAME))
    filepath = os.path.join(PATH, CATALOG_NAME)
    sample = prepare(os.path.join(os.getcwd(),
                                  'tests',
                                  'fixtures',
                                  'download_resourses.html'),
                     URL, PATH)
    for link in tqdm(sample):
        with requests_mock.Mocker(real_http=True) as m:
            m.get(URL)
            content = download_url(link)
            save_file(content, filepath, url=link)
    lenght = len(os.listdir(os.path.join(PATH, CATALOG_NAME)))
    assert lenght == 15
    check = os.path.isfile(os.path.join(PATH, CATALOG_NAME,
                                        'mirf-ru-wp-'
                                        'content-themes-mirf'
                                        '-css-delement.css'))
    assert check is True


def test_find_content():
    sample = prepare(FIXTURE_FIND_FILE,
                     'https://docs.python-requests.org/',
                     PATH)
    assert sample == fixture_list


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


def astest_resourse():
    with open(CONTENT_FIXTURE) as f:
        content = f.read()
        with requests_mock.Mocker() as m:
            m.get(URL_FOR_CONTENT, text=content)
            download_url(URL_FOR_CONTENT)
            save_file(content, PATH, url=URL_FOR_CONTENT)
            with \
                    open(os.path.join(PATH,
                                      'mirf-ru-wp-content-plugins-push'
                                      '-js-push-lib.js')) as q:
                compare = q.read()
                assert compare == content
