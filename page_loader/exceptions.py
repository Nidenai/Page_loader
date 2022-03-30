import os
import requests


def existing_path(catalog):
    """Функция, проверяющий правильность каталога"""
    if not os.path.exists(catalog):
        raise TypeError('Путь не существует')


def check_url_response(url):
    """Функция проверят ссылку на ответ"""
    try:
        url.raise_for_status()
    except requests.exceptions:
        raise requests.exceptions
