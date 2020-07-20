from espconfig import *

debug = config['debug']

#Выводим отладочные сообщения
def dprint(*args):
    if debug: print(*args) 