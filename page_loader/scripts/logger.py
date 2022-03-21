import sys

from loguru import logger


def logger_script():
    logger.remove()
    logger.add(sys.stdout, format="{message}", level="INFO")
