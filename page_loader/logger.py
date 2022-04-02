import os
import sys

from loguru import logger

url_logger_path = os.path.join(os.getcwd(), 'logs', 'url_logger.txt')
html_logger_path = os.path.join(os.getcwd(), 'logs', 'html_logger.txt')


def info_only(record):
    return record["level"].name == "INFO"


def trace_only(record):
    return record["level"].name == "TRACE"


def debug_only(record):
    return record["level"].name == "DEBUG"


def logger_script():
    logger.remove()
    logger.add(sys.stdout, format="{message} - {time}",
               level="INFO", filter=info_only)
    logger.add(url_logger_path, format='{time} : {message}',
               level='DEBUG', filter=debug_only)
    logger.add(html_logger_path, format='{time} : {message}',
               level='TRACE', filter=trace_only)
