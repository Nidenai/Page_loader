import os
from progress.bar import Bar
import requests as re
from bs4 import BeautifulSoup as bs

from page_loader.engine.auxiliary import existing_path, naming_png


def parse_image(data, path_=os.getcwd()):
    data = format_data(finder_image(data))
    with Bar('Collecting images', max=20) as bar:
        for i in range(20):
            for url in data:
                download_image(url, path_)
                bar.next()
    bar.finish()


def finder_image(file):
    result = []
    fp = open(file, 'r', encoding='utf-8')
    content = fp.read()
    soup = bs(content, "html.parser")
    for link in soup.find_all('img'):
        result.append(link.get('src'))
    return result


def download_image(url, path_=os.getcwd()):
    existing_path(path_)
    imagename = naming_png(url)
    filepath = os.path.join(path_, imagename)
    with re.get(url, stream=True) as image:
        with open(filepath, 'wb+') as downloaded_image:
            for chunk in image.iter_content(chunk_size=128):
                downloaded_image.write(chunk)
    downloaded_image.close()


def format_data(list):
    result = []
    for item in list:
        if item.startswith('http'):
            result.append(item)
        elif item.startswith("//"):
            result.append(item.replace("//", 'http://'))
    return result


def naming_path_to_img(url, file):
    f = file.replace('.html', '') + '_files'
    return os.path.join(f, naming_png(url))


def format_path_to_img(file):
    file = os.path.normpath(file)
    file = file.split(os.sep)
    return file[-1]


def replace_html(file):
    with open(file, 'r', encoding='utf-8') as fp:
        content = fp.read()
        soup = bs(content, "html.parser")
        for link in soup.find_all('img'):
            v = link.attrs
            v['src'] = naming_path_to_img(v['src'], format_path_to_img(file))
    with open(file, 'w+', encoding='utf-8') as k:
        k.write(str(soup))
