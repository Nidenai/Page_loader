import os
from urllib.parse import urljoin, urlparse

import requests as re
from bs4 import BeautifulSoup as bs
from loguru import logger

logger.remove()
logger.add(os.path.join(os.getcwd(), 'logs', 'debug.json'),
           format="{message}", level="INFO", rotation="100 MB",
           compression="zip")


class File:
    """Класс для работы с файлами в каталоге"""
    IMG = ('img', 'src')
    SCRIPT = ('script', 'src')
    LINK = ('link', 'href')

    def __init__(self, file):
        self.file = file

    def create_filename(self):
        """Создание имени файла для отображения его в каталоге с ресурсом"""
        name = str(self.file)
        name = name.replace('https://', '')
        name = name.replace('https://', '')
        name = name.replace('http://', '')
        name = name.replace('www.', '')
        name = name.replace('?', '-')
        name = name.replace('/', '-')
        name = name.replace('&', '-')
        name = name.replace(':', '-')
        if name.startswith('--'):
            name = name.replace('--', '', 1)
        elif name.startswith('-'):
            name = name.replace('-', '', 1)
        else:
            pass
        return name

    def create_html_filename(self):
        """Метод создает имя html-файла"""
        return str(File(self.file).create_filename()) + '.html'

    def find_content(self, source, url):
        """Метод собирает в список весь контент по тегам, зашитым в source"""
        result = []
        tag, arg = source
        with open(self.file, 'r', encoding='utf-8') as content:
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


class Dir:
    """Класс работает с каталогами и путями"""

    def __init__(self, catalog):
        self.catalog = catalog

    def create_html_catalog(self):
        """Метод создает каталог для ресурсов страницы"""
        name = self.catalog.replace('.html', '_files')
        if not os.path.exists(name):
            os.mkdir(name)
        else:
            pass

    def is_path_exist(self):
        """Метод, проверяющий правильность каталога
        и создающий его, что бы не было ошибки"""
        path_ = self.catalog
        if not os.path.exists(path_):
            os.makedirs(path_)
        elif path_ == os.path.join('sys'):
            raise TypeError('Нельзя сюда сохранять')
        elif os.path.exists(path_):
            pass


class Url:
    """Класс для работы со ссылками"""

    def __init__(self, url):
        self.url = url

    def check_url_response(self):
        """Метод проверят ссылку на ответ"""
        try:
            re.get(self.url)
        except re.exceptions:
            raise TypeError('Ошибочная ссылка')

    def download(self, path_=os.getcwd(), filename=None):
        """Метод скачивает контент по ссылке,
        по умолчанию в рабочую директорию"""
        url = self.url
        Dir(path_).is_path_exist()
        Url(url).check_url_response()
        if filename is None:
            filename = File(url).create_filename()
        filepath = os.path.join(os.getcwd(), os.path.normpath(path_), filename)
        with re.get(url, stream=True) as temp:
            with open(filepath, 'wb+') as downloaded_file:
                for chunk in temp.iter_content(chunk_size=128):
                    downloaded_file.write(chunk)


v = Url('https://github.com/Delgan/loguru')
d = Dir('var')
f = File('github.com-Delgan-loguru')

# v.download(filename=f.file)
# f.find_content(LINK, v.url)
