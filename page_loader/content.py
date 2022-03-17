import os
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup as bs
from tqdm import tqdm

EMPTY = ''
LINE = '-'
REPLACED = {'https://': EMPTY, 'http://': EMPTY,
            'www.': EMPTY, '?': LINE, '/': LINE,
            '&': LINE, ':': LINE, '.': LINE}


def find_content(file, source, url):
    """Функция собирает в список весь контент по тегам, зашитым в source"""
    result = []
    tag, arg = source
    with open(file, 'r', encoding='utf-8') as content:
        soup = bs(content, 'html.parser')
        for link in soup.find_all(tag):
            if link.get(arg) is not None:
                if not link.get(arg).startswith('http'):
                    q = urljoin(url, link.get(arg))
                    if urlparse(q).netloc == urlparse(url).netloc:
                        result.append(q)
                else:
                    if urlparse(link.get(arg)).netloc == \
                            urlparse(url).netloc:
                        result.append(link.get(arg))
    return result


def create_filename_for_file(name):
    """Функция создает имя для ресурсов страницы"""
    name = str(name)
    filename, file_extension = os.path.splitext(name)
    for key, value in REPLACED.items():
        filename = filename.replace(key, value)
    if filename.startswith('--'):
        filename = filename.replace('--', '', 1)
    elif filename.startswith('-'):
        filename = filename.replace('-', '', 1)
    else:
        pass
    if file_extension == '':
        result = filename + '.html'
    else:
        result = filename + file_extension
    return result


def replace_content(file, source, origin_url, catalog):
    """Функция меняет ссылки на локальные ресурсы в веб-странице"""
    with open(file, 'r', encoding='utf-8') as origin:
        content = bs(origin, 'html.parser')
        for item in tqdm(source, desc='Formatting HTML'):
            tag, arg = item
            for link in content.find_all(tag):
                if link.get(arg) is not None:
                    if not link.get(arg).startswith('http'):
                        q = urljoin(origin_url, link.get(arg))
                        if urlparse(q).netloc == \
                                urlparse(origin_url).netloc:
                            filename = \
                                create_filename_for_file(q)
                            filepath = catalog + '/' + filename
                            link[arg] = filepath
                    else:
                        if urlparse(link.get(arg)).netloc == \
                                urlparse(origin_url).netloc:
                            filename = \
                                create_filename_for_file(link.get(arg))
                            filepath = catalog + '/' + filename
                            link[arg] = filepath
        content = content.prettify()
    with open(file, 'w+', encoding='utf-8') as rewrite_file:
        rewrite_file.write(str(content))
