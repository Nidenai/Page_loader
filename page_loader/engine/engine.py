import requests
import os


def download(url, path_=os.getcwd()):
    filename = naming_file(url)
    filepath = os.path.join(os.getcwd(), to_path(path_), filename)
    existing_path(to_path(path_))
    with requests.get(url, stream=True) as r:
        with open(filepath, 'wb+') as keyfile:
            for chunk in r.iter_content(chunk_size=128):
                keyfile.write(chunk)
    keyfile.close()
    make_catalog(filepath)
    return keyfile


def naming_file(file):  # функция нормализует имя сохраняемой страницы
    v = str(file)
    v = v.replace('https://', '')
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


