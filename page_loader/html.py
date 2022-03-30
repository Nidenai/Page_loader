from bs4 import BeautifulSoup as bs

from page_loader.url import create_link, create_filename_for_file


def prepare(file, source, origin_url, catalog):
    resources = []
    tag, arg = source
    with open(file, 'r', encoding='utf-8') as content:
        soup = bs(content, 'html.parser')
        for link in soup.find_all(tag):
            link_name = create_link(origin_url, link, arg)
            if link_name is not None:
                resources.append(link_name)
                link[arg] = catalog + '/' + create_filename_for_file(link_name)
        final_content = soup.prettify()
    with open(file, 'w+', encoding='utf-8') as rewrite_file:
        rewrite_file.write(str(final_content))
    return resources
