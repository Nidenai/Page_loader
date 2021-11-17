from page_loader.engine.engine import download
import os

HTML_FILE = os.path.join(os.getcwd(),
                         'tests', 'fixtures', 'ru.hexlet.io-courses.html')
URL = 'https://ru.hexlet.io/courses'
NAME = 'ru.hexlet.io-courses.html'
PATH_FOR_FILE = os.path.join('tests', 'var', 'tmp')
CATALOG_NAME = 'ru.hexlet.io-courses_files'


def clear_():
    if os.path.isfile(os.path.join(PATH_FOR_FILE, NAME)):
        os.remove(os.path.join(PATH_FOR_FILE, NAME))
    elif os.path.isdir(os.path.join(PATH_FOR_FILE, CATALOG_NAME)):
        os.rmdir((os.path.join(PATH_FOR_FILE, CATALOG_NAME)))
    else:
        pass


def test_naming():
    clear_()
    test_name = os.path.basename(os.path.join(os.getcwd(),
                                              'fixtures',
                                              'ru.hexlet.io-courses.html'))
    download(URL, PATH_FOR_FILE)
    name = os.path.basename(os.path.join(PATH_FOR_FILE, NAME))
    assert name == test_name


def test_catalog():
    clear_()
    download(URL, PATH_FOR_FILE)
    base_catalog = os.path.basename(os.path.join(os.getcwd(),
                                                 'fixtures',
                                                 'ru.hexlet.io-courses_files'))
    catalog = os.path.basename(os.path.join(PATH_FOR_FILE, CATALOG_NAME))
    assert base_catalog == catalog
