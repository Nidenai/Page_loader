import os
from page_loader.engine.auxiliary import existing_path, naming_png
from bs4 import BeautifulSoup as BS
import requests as re


file = 'tmp/example.html'


def parse_image(data, path_=os.getcwd()):
    data = format_data(finder_image(data))
    for url in data:
        download_image(url, path_)


def finder_image(file):
    result = []
    fp = open(file, 'r', encoding='utf-8')
    content = fp.read()
    soup = BS(content, "html.parser")
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
    return result
