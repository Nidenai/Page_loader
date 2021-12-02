import os
from urllib.parse import urlparse

import requests as re
from bs4 import BeautifulSoup as BS
from progress.bar import Bar

from page_loader.engine.auxiliary import existing_path, \
    naming_script, adding_http


def finder_script(file):
    result = []
    fp = open(file, 'r', encoding='utf-8')
    content = fp.read()
    soup = BS(content, "html.parser")
    for link in soup.find_all('script'):
        if link.get('src') is not None:
            result.append(link.get('src'))
        else:
            pass
    return result


def download_script(data, path_=os.getcwd()):
    existing_path(path_)
    with Bar('Скачиваем скрипты') as bar:
        for i in range(20):
            for url in data:
                o = urlparse(url)
                scriptname = naming_script(o.geturl())
                filepath = os.path.join(path_, scriptname)
                with re.get(adding_http(o.geturl()), stream=True) as r:
                    with open(filepath, 'wb+') as k:
                        for chunk in r.iter_content(chunk_size=128):
                            k.write(chunk)
                            bar.next()
    bar.finish()


def parse_scripts(file, path_=os.getcwd()):
    download_script(finder_script(file), path_)
