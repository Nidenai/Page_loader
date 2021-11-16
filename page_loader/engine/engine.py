import requests
import os


def download(url, path_=os.getcwd()):
    filepath = os.path.join(os.getcwd(), to_path(path_), naming_file(url))
    existing_path(to_path(path_))
    with requests.get(url, stream=True) as r:
        with open(filepath, 'wb+') as kfile:
            for chunk in r.iter_content(chunk_size=128):
                kfile.write(chunk)
    kfile.close()
    return kfile


def naming_file(file):
    v = str(file)
    v = v.replace('https://', '')
    v = v.replace('www.', '')
    result = v.replace('/', '-') + '.html'
    return result


def to_path(path_):
    if path_ == '':
        return path_
    path = os.path.normpath(path_)
    result = path.split(os.sep)
    result = os.path.join(*result)
    return result


def existing_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
    elif os.path.exists(path):
        pass
