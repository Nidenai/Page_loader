import os

import requests

from page_loader.engine.auxiliary import naming_file, to_path, \
    existing_path, make_catalog
from page_loader.engine.constants import IMG, LINK, SCRIPT
from page_loader.engine.content_downloader import parsing


def download(url, path_=os.getcwd()):
    filename = naming_file(url)
    filepath = os.path.join(os.getcwd(), to_path(path_), filename)
    existing_path(to_path(path_))
    with requests.get(url, stream=True) as r:
        with open(filepath, 'wb+') as keyfile:
            for chunk in r.iter_content(chunk_size=128):
                keyfile.write(chunk)
    keyfile.close()
    make_catalog(filepath)
    catalog_name = filepath.replace('.html', '_files')
    parsing(filepath, IMG, catalog_name)
    parsing(filepath, LINK, catalog_name)
    parsing(filepath, SCRIPT, catalog_name)
    return keyfile
