from page_loader.engine.engine import download
from page_loader.cli import function


def main():
    parser = function()
    download(parser.file)


if __name__ == '__main__':
    main()
