import argparse
import os


def function():
    func = argparse.ArgumentParser(description='Page Loader')
    func.add_argument('url', help='Put your link here')
    func.add_argument('-o', '--output', default=os.getcwd())
    args = func.parse_args()
    return args
