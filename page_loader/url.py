import os
from urllib.parse import urljoin, urlparse
from page_loader.logger import logger_script
from loguru import logger

EMPTY = ''
LINE = '-'
REPLACED = {'https://': EMPTY, 'http://': EMPTY,
            'www.': EMPTY, '?': LINE, '/': LINE,
            '&': LINE, ':': LINE, '.': LINE}


def create_filename_for_file(name):
    logger_script()
    """Функция создает имя для ресурсов страницы"""
    name = str(name)
    filename, file_extension = os.path.splitext(name)
    for key, value in REPLACED.items():
        filename = filename.replace(key, value)
    if filename.startswith('--'):
        filename = filename.replace('--', '', 1)
    elif filename.startswith('-'):
        filename = filename.replace('-', '', 1)
    if file_extension == '':
        result = filename + '.html'
    else:
        result = filename + file_extension
    logger.debug(f'Result of create_filename function: {result}')
    return result


def create_link(url, link, arg):
    logger_script()
    result = None
    if link.get(arg) is not None:
        if not link.get(arg).startswith('http'):
            name = urljoin(url, link.get(arg))
            if urlparse(name).netloc == urlparse(url).netloc:
                result = name
                logger.debug(f'Result of create_link function: {result}')
        else:
            if urlparse(link.get(arg)).netloc == urlparse(url).netloc:
                result = link.get(arg)
                logger.debug(f'Result of create_link function: {result}')
    return result
