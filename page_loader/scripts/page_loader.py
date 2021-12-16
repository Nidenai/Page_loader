from page_loader.engine.download import download
from page_loader.cli import function


def main():
    parser = function()
    download(parser.url, parser.output)


if __name__ == '__main__':
    main()
