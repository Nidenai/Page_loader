import os
import requests
import requests_mock


def existing_path(catalog):
    """Функция, проверяющий правильность каталога"""
    if not os.path.exists(catalog):
        raise TypeError('Путь не существует')


def check_url_response(url):
    """Функция проверят ссылку на ответ"""
    try:
        with requests_mock.Mocker() as m:
            m.get(url)
            requests.get(url).status_code
    except requests.exceptions:
        raise TypeError('Ошибочная ссылка')
