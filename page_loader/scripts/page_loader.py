import requests
import os


def download(url):
    with requests.get(url, stream=True) as r:
        with open(os.path.join(os.getcwd(), naming_file(url)), 'wb') as keyfile:
            for chunk in r.iter_content(chunk_size=128):
                keyfile.write(chunk)
    keyfile.close()
    return keyfile


def naming_file(file):
    v = str(file)
    var = v.replace('https://', '')
    result = var.replace('/', '-') + '.html'
    return result


def main():
    download(url)


if __name__ == '__main__':
    main()
