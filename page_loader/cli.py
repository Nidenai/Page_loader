import argparse
import os


def function():
    func = argparse.ArgumentParser(description='Page Loader')
    func.add_argument('file')
    func.add_argument('--output', default=os.getcwd())
    func.add_argument('-V', '--version',
                      action='version',
                      version="%(prog)s 0.10.2")
    args = func.parse_args()
    return args
