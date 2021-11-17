from page_loader.engine.engine import download
import os


HTML_FILE = os.path.join(os.getcwd(),
                         'tests', 'fixtures', 'ru.hexlet.io-courses.html')
URL = 'https://ru.hexlet.io/courses'
NAME = 'ru.hexlet.io-courses.html'
PATH_FOR_FILE = os.path.join('tests', 'var', 'tmp')


def clear_experiment():
    if os.path.isfile(os.path.join(PATH_FOR_FILE, NAME)):
        os.remove(os.path.join(PATH_FOR_FILE, NAME))
    else:
        pass

def test_naming():
    clear_experiment()
    test_name = os.path.basename(os.path.join(os.getcwd(),
                                              'fixtures',
                                              'ru.hexlet.io-courses.html'))
    download(URL, PATH_FOR_FILE)
    name = os.path.basename(os.path.join(PATH_FOR_FILE,
                                         'ru.hexlet.io-courses.html'))
    assert name == test_name
