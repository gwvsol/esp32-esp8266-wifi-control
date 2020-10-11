from espconfig import *

"""Здесь реализованы методы для использования во всем проекте"""

debug = config['debug']

#Выводим отладочные сообщения
def dprint(*args):
    if debug: print(*args) 