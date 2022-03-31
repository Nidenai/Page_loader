import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from page_loader.logger import logger_script
from loguru import logger

from page_loader.url import create_link, create_filename_for_file


def prepare(file, origin_url, catalog):
    logger_script()
    IMG = ('img', 'src')
    SCRIPT = ('script', 'src')
    LINK = ('link', 'href')
    LIST_ = [IMG, SCRIPT, LINK]
    resources = []
    content = requests.get(origin_url).content
    soup = bs(content, 'html.parser')
    for item in LIST_:
        tag, arg = item
        for link in tqdm(soup.find_all(tag)):
            link_name = create_link(origin_url, link, arg)
            if link_name is not None:
                resources.append(link_name)
                link[arg] = catalog + '/' + create_filename_for_file(link_name)
    final_content = soup.prettify()
    with open(file, 'w+', encoding='utf-8') as rewrite_file:
        rewrite_file.write(str(final_content))
    logger.trace(f'List of getting resourses: {resources}')
    return resources
