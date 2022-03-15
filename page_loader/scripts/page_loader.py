from page_loader.cli import function
from page_loader.download import download


def main():
    parser = function()
    download(parser.url, parser.output)


if __name__ == '__main__':
    main()
