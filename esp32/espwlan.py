import gc, network
import uasyncio as asyncio
from espconfig import *
from esputils import dprint
gc.collect()                                #Очищаем RAM

class WiFiConnect(object):

    def __init__(self):
        self.dprint     = dprint
        self.mode       = config['wifiMode']                        # False = AP, True = ST
        self.connect    = config['connect']                         # False = Подключения нет, True = Подключение к сети WiFi
        self.debug      = config['debug']
        if self.wifi: self.station = network.WLAN(network.STA_IF)   # ST Mode
        else: self.wifi = network.WLAN(network.AP_IF)               # AP Mode