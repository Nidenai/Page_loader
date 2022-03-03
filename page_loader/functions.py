import os
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup as bs
from loguru import logger
from tqdm import tqdm

logger.remove()
logger.add(os.path.join(os.getcwd(), 'logs', 'debug.json'),
           format="{message}", level="INFO", rotation="100 MB",
           compression="zip")


def create_filename(filename):
    """Создание имени файла для отображения его в каталоге с ресурсом"""
    name = str(filename)
    name = name.replace('https://', '')
    name = name.replace('https://', '')
    name = name.replace('http://', '')
    name = name.replace('www.', '')
    name = name.replace('?', '-')
    name = name.replace('/', '-')
    name = name.replace('&', '-')
    name = name.replace(':', '-')
    name = name.replace('.', '-')
    name = name.replace('-html', '.html')
    if name.startswith('--'):
        name = name.replace('--', '', 1)
    elif name.startswith('-'):
        name = name.replace('-', '', 1)
    else:
        pass
    return name


def create_html_filename(name):
    """Функция создает имя html-файла"""
    return str(create_filename(name)) + '.html'


def find_content(file, source, url):
    """Функция собирает в список весь контент по тегам, зашитым в source"""
    result = []
    tag, arg = source
    with open(file, 'r', encoding='utf-8') as content:
        soup = bs(content, 'html.parser')
        for link in soup.find_all(tag):
            if link.get(arg) is not None:
                logger.info('Raw argument: ' + str(link.get(arg)))
                if not link.get(arg).startswith('http'):
                    q = urljoin(url, link.get(arg))
                    if urlparse(q).netloc == urlparse(url).netloc:
                        result.append(q)
                        logger.info('Clear argument: ' + q)
                else:
                    if urlparse(link.get(arg)).netloc == \
                            urlparse(url).netloc:
                        result.append(link.get(arg))
                        logger.info('Clear argument: ' + (link.get(arg)))
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
                                create_filename(q)
                            filepath = os.path.join(os.path.normpath
                                                    (catalog), filename)
                            link[arg] = filepath
                    else:
                        if urlparse(link.get(arg)).netloc == \
                                urlparse(origin_url).netloc:
                            filename = \
                                create_filename(link.get(arg))
                            filepath = \
                                os.path.join(os.path.normpath(catalog),
                                             filename)
                            link[arg] = filepath
    with open(file, 'w+', encoding='utf-8') as rewrite_file:
        rewrite_file.write(str(content))


def create_html_catalog(catalog):
    """Функция создает каталог для ресурсов страницы"""
    name = catalog.replace('.html', '_files')
    if not os.path.exists(name):
        os.mkdir(name)
    else:
        pass


def is_path_exist(catalog):
    """Функция, проверяющий правильность каталога
    и создающий его, что бы не было ошибки"""
    path_ = catalog
    if not os.path.exists(path_):
        os.makedirs(path_)
    elif path_ == os.path.join('sys'):
        raise TypeError('Нельзя сюда сохранять')
    elif os.path.exists(path_):
        pass


def check_url_response(url):
    """Функция проверят ссылку на ответ"""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions:
        raise TypeError('Ошибочная ссылка')


def download_url(url, path_=os.getcwd(), filename=None):
    """Функция скачивает контент по ссылке,
    по умолчанию в рабочую директорию"""
    is_path_exist(path_)
    check_url_response(url)
    if filename is None:
        filename = create_filename(url)
    filepath = os.path.join(os.getcwd(), os.path.normpath(path_), filename)
    with requests.get(url, stream=True) as temp:
        with open(filepath, 'wb+') as downloaded_file:
            for chunk in temp.iter_content(chunk_size=128):
                downloaded_file.write(chunk)
