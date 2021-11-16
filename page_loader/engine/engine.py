import requests
import os


def download(url):
    with requests.get(url, stream=True) as r:
        with open(os.path.join(os.getcwd(), naming_file(url)), 'wb') as kfile:
            for chunk in r.iter_content(chunk_size=128):
                kfile.write(chunk)
    kfile.close()
    return kfile


def naming_file(file):
    v = str(file)
    v = v.replace('https://', '')
    result =v.replace('/', '-') + '.html'
    return result
