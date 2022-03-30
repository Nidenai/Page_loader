import os

import requests
from loguru import logger
from tqdm import tqdm

from page_loader.exceptions import check_url_response, existing_path
from page_loader.html import prepare
from page_loader.logger import logger_script
from page_loader.url import create_filename_for_file


def download_url(url):
    link = requests.get(url)
    check_url_response(link)
    content = link.content
    return content


def save_file(content, path_=os.getcwd(), filename=None, url=None):
    existing_path(path_)
    if filename is None:
        filename = create_filename_for_file(url)
    filepath = os.path.join(os.getcwd(), os.path.normpath(path_), filename)
    with open(filepath, 'wb+') as downloaded_file:
        downloaded_file.write(content)


def download(url, path_=os.getcwd()):
    logger_script()
    filename = create_filename_for_file(url)
    main_page = download_url(url)
    save_file(main_page, path_, filename)
    logger.info(f'Resource by {url}] was downloaded: {filename}')
    filepath = os.path.join(os.getcwd(), os.path.normpath(path_), filename)
    catalog = os.path.normpath(filepath).replace('.html', '_files')
    if not os.path.exists(catalog):
        os.mkdir(catalog)
    catalog_name = os.path.basename(str(catalog))
    resourses = prepare(filepath, url, catalog_name)
    for link in tqdm(resourses, desc='Download Files', unit=' kb'):
        try:
            content = download_url(link)
            save_file(content, catalog, url=link)
        except Exception:
            logger.info(f'Link {link} cannot be downloaded')
    logger.info(f"Done. You can open saved page from: {filepath}")
    return filepath
