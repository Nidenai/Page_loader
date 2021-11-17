from page_loader.engine.engine import download
import os


HTML_FILE = os.path.join(os.getcwd(),
                         'tests', 'fixtures', 'ru.hexlet.io-courses.html')
URL = 'https://ru.hexlet.io/courses'
NAME = 'ru.hexlet.io-courses.html'


def test_naming():
    test_name = os.path.basename(os.path.join(os.getcwd(),
                                              'fixtures',
                                              'ru.hexlet.io-courses.html'))
    download(URL)
    name = os.path.basename(os.path.join(os.getcwd(),
                                         'ru.hexlet.io-courses.html'))
    assert name == test_name


def test_content():
