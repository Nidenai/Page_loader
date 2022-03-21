from bs4 import BeautifulSoup as bs
from tqdm import tqdm

from page_loader.url import create_link, create_filename_for_file


def find_content(file, source, url):
    """Функция собирает в список весь контент по тегам, зашитым в source"""
    result = []
    tag, arg = source
    with open(file, 'r', encoding='utf-8') as content:
        soup = bs(content, 'html.parser')
        for link in soup.find_all(tag):
            link_name = create_link(url, link, arg)
            if link_name is not None:
                result.append(link_name)
    return result


def replace_content(file, source, origin_url, catalog):
    """Функция меняет ссылки на локальные ресурсы в веб-странице"""
    with open(file, 'r', encoding='utf-8') as origin:
        content = bs(origin, 'html.parser')
        for item in tqdm(source, desc='Formatting HTML'):
            tag, arg = item
            for link in content.find_all(tag):
                link_name = create_link(origin_url, link, arg)
                if link_name is not None:
                    link[arg] = \
                        catalog + '/' + \
                        create_filename_for_file(link_name)
        content = content.prettify()
    with open(file, 'w+', encoding='utf-8') as rewrite_file:
        rewrite_file.write(str(content))
