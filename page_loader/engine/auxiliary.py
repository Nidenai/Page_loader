import os


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


def naming_png(url):
    v = str(url)
    v = v.replace('https://', '')
    v = v.replace('http://', '')
    v = v.replace('www.', '')
    v = v.replace('?', '-')
    if v.endswith(('.png', '.jpg', '.jpeg')):
        pass
    else:
        v = v + '.png'
    v = v.replace('/', '-')
    if v.startswith('--'):
        v = v.replace('--', '', 1)
    elif v.startswith('-'):
        v = v.replace('-', '', 1)
    else:
        pass
    result = v
    return result
