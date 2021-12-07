import os
from urllib.parse import urlparse

import requests as re
from bs4 import BeautifulSoup as bs
from progress.bar import Bar

from page_loader.engine.auxiliary import existing_path, \
    naming_script, adding_http, format_path_to_source, naming_path_to_source


def finder_html(file):
    result = []
    fp = open(file, 'r', encoding='utf-8')
    content = fp.read()
    soup = bs(content, "html.parser")
    for link in soup.find_all('link'):
        if link.get('href'):
            result.append(link.get('href'))
        else:
            pass
    return result


def download_link(data, path_=os.getcwd()):
    existing_path(path_)
    with Bar('Скачиваем ссылки') as bar:
        for url in data:
            for i in range(2):
                o = urlparse(url)
                scriptname = naming_script(o.geturl())
                filepath = os.path.join(path_, scriptname)
                with re.get(adding_http(o.geturl()), stream=True) as r:
                    with open(filepath, 'wb+') as k:
                        for chunk in r.iter_content(chunk_size=128):
                            k.write(chunk)
                            bar.next()
    bar.finish()


def parse_links(file, path_=os.getcwd()):
    data = finder_html(file)
    download_link(data, path_)


def replace_link(file):
    with open(file, 'r', encoding='utf-8') as fp:
        content = fp.read()
        soup = bs(content, "html.parser")
        for link in soup.find_all('link'):
            v = link.attrs
            v['href'] = naming_path_to_source(v['href'],
                                              format_path_to_source(file))
    with open(file, 'w+', encoding='utf-8') as k:
        k.write(str(soup))
