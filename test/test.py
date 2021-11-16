from constants import URL
from page_loader.engine.engine import download
import os


def test_naming():
    test_name = os.path.basename(os.path.join(os.getcwd(),
                                              'fixtures',
                                              'ru.hexlet.io-courses.html'))
    download(URL)
    name = os.path.basename(os.path.join(os.getcwd(),
                                         'ru.hexlet.io-courses.html'))
    assert name == test_name
