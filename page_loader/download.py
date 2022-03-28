import os

import requests
from loguru import logger
from tqdm import tqdm

from page_loader.exceptions import check_url_response, existing_path
from page_loader.html import find_content, replace_content
from page_loader.logger import logger_script
from page_loader.url import create_filename_for_file

IMG = ('img', 'src')
SCRIPT = ('script', 'src')
LINK = ('link', 'href')
LIST_ = [IMG, SCRIPT, LINK]


def download_url(url, path_=os.getcwd(), filename=None):
    """Функция скачивает контент по ссылке,
    по умолчанию в рабочую директорию"""
    existing_path(path_)
    if filename is None:
        filename = create_filename_for_file(url)
    filepath = os.path.join(os.getcwd(), os.path.normpath(path_), filename)
    with requests.get(url, stream=True) as temp:
        check_url_response(temp)
        with open(filepath, 'wb+') as downloaded_file:
            for chunk in temp.iter_content(chunk_size=128):
                downloaded_file.write(chunk)


def download(url, path_=os.getcwd()):
    logger_script()
    filename = create_filename_for_file(url)
    try:
        download_url(url, path_, filename)
        logger.info(f'Resource by {url}] was downloaded: {filename}')
    except Exception:
        raise Exception
    filepath = os.path.join(os.getcwd(), os.path.normpath(path_), filename)
    catalog = os.path.normpath(filepath).replace('.html', '_files')
    if not os.path.exists(catalog):
        os.mkdir(catalog)
    catalog_name = os.path.basename(str(catalog))
    downloaded_list = []
    for item in tqdm(LIST_, desc='Getting resourses'):
        sample = find_content(filepath, item, url)
        downloaded_list = downloaded_list + sample
    logger.info(downloaded_list)
    replace_content(filepath, LIST_, url, catalog_name)
    try:
        for link in tqdm(downloaded_list, desc='Download Files', unit=' kb'):
            download_url(link, catalog)
    except Exception:
        logger.info('Что-то не скачивается')
    logger.info(f"Done. You can open saved page from: {filepath}")
    return filepath
