import os

import requests


def naming_file(file):  # функция нормализует имя сохраняемой страницы
    v = str(file)
    v = v.replace('https://', '')
    v = v.replace('http://', '')
    v = v.replace('www.', '')
    result = v.replace('/', '-') + '.html'
    return result


def to_path(path_):  # функция нормализует введенный пользователем путь
    if path_ == '':
        return path_
    path = os.path.normpath(path_)
    result = path.split(os.sep)
    result = os.path.join(*result)
    return result


def existing_path(path):  # функция проверяет, существует ли путь
    if not os.path.exists(path):
        os.makedirs(path)
    elif os.path.exists(path):
        pass


def make_catalog(name):
    name = name.replace('.html', '') + '_files'
    if not os.path.exists(name):
        os.mkdir(name)
    else:
        pass


def check_response(url):
    if requests.get(url).status_code == 200:
        pass
    else:
        raise TypeError('Хост не отвечает')


def check_folder(path_):
    if path_ == '/sys':
        raise TypeError('Некорректный путь')
    elif not os.path.exists(path):
        raise TypeError('Путь не существует')
