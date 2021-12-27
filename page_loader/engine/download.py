import os

import requests
from loguru import logger
from page_loader.engine.auxiliary import naming_file, to_path, \
    existing_path, make_catalog
from page_loader.engine.constants import IMG, LINK, SCRIPT
from page_loader.engine.content_downloader import parsing
from progress.bar import Bar
from page_loader.engine.auxiliary import check_response


def download(url, path_=os.getcwd()):
    check_response(url)
    filename = naming_file(url)
    logger.remove()
    logger.add('debug.json', format='{time}, {level}, {message}',
               level="DEBUG", rotation='100 Kb')
    logger.debug(filename)
    filepath = os.path.join(os.getcwd(), to_path(path_), filename)
    logger.debug(filepath)
    existing_path(to_path(path_))
    with requests.get(url, stream=True) as r:
        with open(filepath, 'wb+') as keyfile:
            for chunk in r.iter_content(chunk_size=128):
                keyfile.write(chunk)
    keyfile.close()
    make_catalog(filepath)
    catalog_name = filepath.replace('.html', '_files')
    with Bar('Progress', max=3) as bar:
        parsing(filepath, IMG, url, catalog_name)
        bar.next()
        parsing(filepath, LINK, url, catalog_name)
        bar.next()
        parsing(filepath, SCRIPT, url, catalog_name)
        bar.next()
    bar.finish()
    return keyfile
