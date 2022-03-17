import os
import requests


def is_path_exist(catalog):
    """Функция, проверяющий правильность каталога"""
    if not os.path.exists(catalog):
        raise TypeError('Путь не существует')
    elif catalog == os.path.join('sys'):
        raise TypeError('Нельзя сюда сохранять')
    elif os.path.exists(catalog):
        pass


def check_url_response(url):
    """Функция проверят ссылку на ответ"""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions:
        raise TypeError('Ошибочная ссылка')
