import os

from loguru import logger

from page_loader.engine.classes import Url, Dir, File


def download_content(filepath, path_, source, url):
    sample = File(filepath).find_content(source, url)
    logger.info('List: ' + str(sample))
    for link in sample:
        Url(link).download(path_)


def download(url, path_=os.getcwd()):
    logger.remove()
    logger.add(os.path.join(os.getcwd(), 'logs', 'debug.json'),
               format="{message}", level="INFO", rotation="10 MB",
               compression="zip")
    filename = File(url).create_html_filename()
    Url(url).download(path_, filename)
    logger.info('This is filename: ' + str(filename))
    filepath = os.path.join(os.getcwd(), os.path.normpath(path_), filename)
    logger.info('This is path: ' + str(filepath))
    Dir(filepath).create_html_catalog()
    catalog = os.path.normpath(filepath).replace('.html', '_files')
    logger.info('This is folder: ' + str(catalog))
    args = [File.LINK, File.IMG, File.SCRIPT]
    for item in args:
        download_content(filepath, catalog, item, url)
    File(filepath).replace_content(File.LIST_, url, path_)


url = 'https://github.com/Delgan/loguru'

download(url, 'var/tmp')

# path_ = 'var/tmp/github.com-Delgan-loguru_files'
# filepath = 'var/tmp/github.com-Delgan-loguru.html'
# download_content(filepath, path_, File.LINK, url)
