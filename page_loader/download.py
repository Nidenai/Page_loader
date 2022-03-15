import os

from loguru import logger
from tqdm import tqdm

import page_loader.functions as functions
from page_loader.Constants import LIST_


def download_content(filepath, path_, source, url):
    sample = functions.find_content(filepath, source, url)
    logger.info('List: ' + str(sample))
    for link in tqdm(sample, desc='Download Files', unit=' kb'):
        functions.download_url(link, path_)


def download(url, path_=os.getcwd()):
    try:
        logger.remove()
        logger.add(os.path.join(os.getcwd(), 'logs', 'log.txt'),
                   format="{message}", level="INFO", rotation="10 MB",
                   compression="zip")
        filename = functions.create_filename(url)
        functions.download_url(url, path_, filename)
        logger.info(f'Resource by {url}] was downloaded: {filename}')
        filepath = os.path.join(os.getcwd(), os.path.normpath(path_), filename)
        functions.create_html_catalog(filepath)
        catalog = os.path.normpath(filepath).replace('.html', '_files')
        catalog_name = os.path.basename(str(catalog))
        args = LIST_
        for item in args:
            download_content(filepath, catalog, item, url)
        functions.replace_content(filepath, LIST_, url, catalog_name)
        logger.info(f"Done. You can open saved page from: {filepath}")
        return filepath
    except Exception:
        raise TypeError('Ошибка')
