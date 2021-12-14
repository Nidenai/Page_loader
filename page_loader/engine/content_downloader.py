import os
import random

import requests as re
from bs4 import BeautifulSoup as bs
from progress.bar import Bar
from page_loader.engine.auxiliary import existing_path

pull = ['Создаем красоту', 'Скачиваем всякое',
        "Лепим нелепимое", "Сохраняем все на ваш компьютер",
        "Воруем у укравших", "Ищем ляпы"]

RANDOM_FOR_BAR = random.choice(pull)


def finder(file, source):
    result = []
    content = open(file, 'r', encoding='utf-8').read()
    soup = bs(content, 'html.parser')
    tag, arg = source
    for link in soup.find_all(tag):
        if link.get(arg) is not None:
            result.append(link.get(arg))
    return result


def download_content(url, path_=os.getcwd()):
    existing_path(path_)
    imagename = naming_file(url)
    filepath = os.path.join(path_, imagename)
    with re.get(url, stream=True) as image:
        with open(filepath, 'wb+') as downloaded_image:
            for chunk in image.iter_content(chunk_size=128):
                downloaded_image.write(chunk)
    downloaded_image.close()


def naming_file(url):
    v = str(url)
    v = v.replace('https://', '')
    v = v.replace('http://', '')
    v = v.replace('www.', '')
    v = v.replace('?', '-')
    v = v.replace('/', '-')
    if v.startswith('--'):
        v = v.replace('--', '', 1)
    elif v.startswith('-'):
        v = v.replace('-', '', 1)
    else:
        pass
    result = v
    return result


def replace(file, source):
    tag, arg = source
    with open(file, 'r', encoding='utf-8') as fp:
        content = fp.read()
        soup = bs(content, "html.parser")
        for link in soup.find_all(tag):
            v = link.attrs
            q = v.get(arg)
            v[arg] = naming_path_to_source(q, format_path_to_source(file))
    with open(file, 'w+', encoding='utf-8') as k:
        k.write(str(soup))


def format_path_to_source(file):
    file = os.path.normpath(file)
    file = file.split(os.sep)
    return file[-1]


def naming_path_to_source(url, file):
    f = file.replace('.html', '') + '_files'
    return os.path.join(f, naming_file(url))


def parsing(file, source, path_=os.getcwd()):
    data = finder(file, source)
    count = len(data)
    with Bar('Progress', max=count) as bar:
        for url in data:
            for i in range(count):
                download_content(url, path_)
                bar.next()
    bar.finish()
    replace(file, source)


