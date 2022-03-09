IMG = ('img', 'src')
SCRIPT = ('script', 'src')
LINK = ('link', 'href')
LIST_ = [IMG, SCRIPT, LINK]
EMPTY = ''
LINE = '-'

REPLACED = {'https://': EMPTY, 'http://': EMPTY,
            'www.': EMPTY, '?': LINE, '/': LINE,
            '&': LINE, ':': LINE, '.': LINE}
