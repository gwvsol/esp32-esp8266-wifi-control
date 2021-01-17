from time import localtime
from espconfig import *

"""Здесь реализованы методы для использования во всем проекте"""

debug = config['debug']

def log(*args):
    """Метод для логирования данных приложения"""
    local = localtime()
    year = local[0]
    month = local[1] if local[1] >= 10 else '0{}'.format(local[1])
    day = local[2] if local[2] >= 10 else '0{}'.format(local[2])
    hour = local[3] if local[3] >= 10 else '0{}'.format(local[3])
    minute = local[4] if local[4] >= 10 else '0{}'.format(local[4])
    second = local[5] if local[5] >= 10 else '0{}'.format(local[5])
    if debug: print('{}-{}-{} {}:{}:{} #'.format(year, month, day, hour, minute, second), *args)

