import os

import requests
from loguru import logger
from tqdm import tqdm

from page_loader.content import find_content, \
    create_filename_for_file, replace_content
from page_loader.exceptions import check_url_response, is_path_exist

IMG = ('img', 'src')
SCRIPT = ('script', 'src')
LINK = ('link', 'href')
LIST_ = [IMG, SCRIPT, LINK]


def create_html_catalog(catalog):
    """Функция создает каталог для ресурсов страницы"""
    name = catalog.replace('.html', '_files')
    if not os.path.exists(name):
        os.mkdir(name)
    else:
        pass


def download_url(url, path_=os.getcwd(), filename=None):
    """Функция скачивает контент по ссылке,
    по умолчанию в рабочую директорию"""
    is_path_exist(path_)
    check_url_response(url)
    if filename is None:
        filename = create_filename_for_file(url)
    filepath = os.path.join(os.getcwd(), os.path.normpath(path_), filename)
    with requests.get(url, stream=True) as temp:
        with open(filepath, 'wb+') as downloaded_file:
            for chunk in temp.iter_content(chunk_size=128):
                downloaded_file.write(chunk)


def download_content(filepath, path_, source, url):
    sample = find_content(filepath, source, url)
    logger.info('List: ' + str(sample))
    for link in tqdm(sample, desc='Download Files', unit=' kb'):
        download_url(link, path_)


def download(url, path_=os.getcwd()):
    try:
        logger.remove()
        logger.add(os.path.join(os.getcwd(), 'logs', 'log.txt'),
                   format="{message}", level="INFO", rotation="10 MB",
                   compression="zip")
        filename = create_filename_for_file(url)
        download_url(url, path_, filename)
        logger.info(f'Resource by {url}] was downloaded: {filename}')
        filepath = os.path.join(os.getcwd(), os.path.normpath(path_), filename)
        create_html_catalog(filepath)
        catalog = os.path.normpath(filepath).replace('.html', '_files')
        catalog_name = os.path.basename(str(catalog))
        args = LIST_
        for item in args:
            download_content(filepath, catalog, item, url)
        replace_content(filepath, LIST_, url, catalog_name)
        print(f"Done. You can open saved page from: {filepath}")
        return filepath
    except Exception:
        raise TypeError('Ошибка')
