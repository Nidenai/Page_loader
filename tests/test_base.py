import os
import shutil

from page_loader import download

URL = 'https://ru.hexlet.io/courses'
NAME = 'ru.hexlet.io-courses.html'
PATH_FOR_FILE = os.path.join(os.getcwd(), 'tests', 'tmp')
CATALOG_NAME = 'ru.hexlet.io-courses_files'


def create_dir():
    catalog = os.path.join(os.getcwd(), 'tests', 'tmp')
    if not os.path.exists(catalog):
        os.mkdir(os.path.join(os.getcwd(), 'tests', 'tmp'))
    else:
        pass


def clear_():
    if os.path.isfile(os.path.join(PATH_FOR_FILE, NAME)):
        os.remove(os.path.join(PATH_FOR_FILE, NAME))
    else:
        pass
    if os.path.isdir(os.path.join(PATH_FOR_FILE, CATALOG_NAME)):
        shutil.rmtree((os.path.join(PATH_FOR_FILE, CATALOG_NAME)))
    else:
        pass


def test_naming():
    clear_()
    create_dir()
    test_name = os.path.basename(os.path.join(os.getcwd(),
                                              'fixtures',
                                              'example.html'))
    download(URL, PATH_FOR_FILE)
    name = os.path.basename(os.path.join(PATH_FOR_FILE, NAME))
    assert name == test_name


def test_catalog():
    clear_()
    create_dir()
    download(URL, PATH_FOR_FILE)
    base_catalog = os.path.basename(os.path.join(os.getcwd(),
                                                 'fixtures',
                                                 'ru.hexlet.io-courses_files'))
    catalog = os.path.basename(os.path.join(PATH_FOR_FILE, CATALOG_NAME))
    assert base_catalog == catalog


def test_content():
    clear_()
    create_dir()
    download(URL, PATH_FOR_FILE)
    base_content = open(os.path.join(os.getcwd(),
                                     'fixtures',
                                     'ru.hexlet.io-courses.html', 'r'))
    compare_content = open(os.path.join(PATH_FOR_FILE, NAME), 'r')
    assert base_content == compare_content
