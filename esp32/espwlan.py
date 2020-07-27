import gc, network
import uasyncio as asyncio
from espconfig import *
from esputils import dprint
gc.collect()                                #Очищаем RAM

class WiFiConnect(object):

    def __init__(self):
        self.dprint     = dprint
        self.mode       = config['mode']        # False = AP, True = ST
        self.debug      = config['debug']
        self.connect    = False                 # False = Подключения нет, True = Подключение к сети WiFi
        self.ip         = "xxx.xxx.xxx.xxx"     # IP адрес полученный c DHCP роутера
        

    
    #Подключение к сети WiFi или поднятие точки доступа
    async def setWlan(self):
        """Метод для активации режимов работы WiFi модуля"""
        if self.mode: 
            self.wifi = network.WLAN(network.STA_IF)   # ST Mode
            self.ssid, self.passwd = config['stssid'], config['stpasswd']
        else: 
            self.wifi = network.WLAN(network.AP_IF)    # AP Mode
            self.ssid, self.passwd = config['apssid'], config['appasswd']
        network.phy_mode(network.MODE_11B)      # network.phy_mode = MODE_11B
        self.wifi.active(True)                  # activate the interface
        if self.mode: await self.setSTMode()
        else: pass


    async def setSTMode(self):
        """Метод для подключения к точке доступа"""
        if not self.wifi.isconnected():
            self.wifi.connect(self.ssid, self.passwd)
        while self.wifi.status() == network.STAT_CONNECTING:
            self.dprint('Connecting to WiFi...')
            await asyncio.sleep(1)
        if self.wifi.status() == network.STAT_GOT_IP:
            self.dprint('WiFi: Connection successfully!')
            self.ip = self.wifi.ifconfig()[0]
            self.connect = True                 # соединение успешно установлено
            self.dprint('WiFi:', self.ip)


    async def setAPMode(self):
        """Метод для включения на миктрокотроллере режима точки доступа"""


