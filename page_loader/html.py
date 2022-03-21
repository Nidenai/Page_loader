from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup as bs
from loguru import logger
from tqdm import tqdm

from page_loader.scripts.logger import logger_script
from page_loader.url import create_filename_for_file, create_link


def find_content(file, source, url):
    """Функция собирает в список весь контент по тегам, зашитым в source"""
    logger_script()
    result = []
    tag, arg = source
    with open(file, 'r', encoding='utf-8') as content:
        soup = bs(content, 'html.parser')
        for link in soup.find_all(tag):
            link_name = create_link(url, link, arg)
            if link_name is not None:
                result.append(link_name)
    logger.info(result)
    return result


def replace_content(file, source, origin_url, catalog):
    """Функция меняет ссылки на локальные ресурсы в веб-странице"""
    with open(file, 'r', encoding='utf-8') as origin:
        content = bs(origin, 'html.parser')
        for item in tqdm(source, desc='Formatting HTML'):
            tag, arg = item
            for link in content.find_all(tag):
                if link.get(arg) is not None:
                    if not link.get(arg).startswith('http'):
                        q = urljoin(origin_url, link.get(arg))
                        if urlparse(q).netloc == \
                                urlparse(origin_url).netloc:
                            filename = \
                                create_filename_for_file(q)
                            filepath = catalog + '/' + filename
                            link[arg] = filepath
                    else:
                        if urlparse(link.get(arg)).netloc == \
                                urlparse(origin_url).netloc:
                            filename = \
                                create_filename_for_file(link.get(arg))
                            filepath = catalog + '/' + filename
                            link[arg] = filepath
        content = content.prettify()
    with open(file, 'w+', encoding='utf-8') as rewrite_file:
        rewrite_file.write(str(content))
