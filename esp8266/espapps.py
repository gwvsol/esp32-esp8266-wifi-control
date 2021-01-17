import gc
import uasyncio as asyncio
from machine import Pin, freq
from espconfig import *
from esputils import log
from espwlan import WiFiConnect

"""Здесь реализуется основное приложение
   подключена работа wifi модуля и его управление 
   а так же вывод основной информации о работе микроконтроллера"""

class MainApps(object):

    def __init__(self):
        self.log             = log
        self.debug           = config['debug']
        self.mode            = config['mode']
        self.ledBoard        = config['wifiLedPin']
        self.ledBoardDefault = config['wifiLedDefault']
        self.wifiLed         = Pin(self.ledBoard, Pin.OUT, value = self.ledBoardDefault)    # Cветодиод для индикации работы WiFi
        self.wifi            = WiFiConnect(led=self.wifiLed)                                # Настрока сети
    
    async def main_loop(self):
        """Метод для вывода служебной отладочной информации"""
        while True:
            mode = 'Station' if self.mode else 'Access Point'      # Подготовка информации о режиме работы WiFi модуля
            # connect = 'Connect' if self.connect else 'Disconnect'  # Подготовка информации о соединении
            gc.collect()                                           # Очищаем RAM
            try:
                # self.log('################# DEBUG MESSAGE #################')
                self.log('MainApps => MemFree:', '{}Kb'.format(round(gc.mem_free()/1024, 2)))       # Свободная память
                self.log('MainApps => MemAllocated:', '{}Kb'.format(round(gc.mem_alloc()/1024, 2))) # Доступная помять
                # self.log('FREQ:', '{}MHz'.format(freq()/1000000))
                self.log('MainApps => WiFi Mode:', mode)
                # self.log('WiFi:', connect)
                self.log('MainApps => IP:', '{}'.format(self.wifi.ip))                              # IP адрес ESP8266
                # self.log('################# DEBUG MESSAGE END #################')
            except Exception as err:
                self.log('MainApps => Exception occurred: ', err)
            await asyncio.sleep(60)


    async def main(self):
        while True:
            try:
                await self.wifi.setWlan()                           # Включение настройки сети
                await self.main_loop()                              # Вывод служебной информации
            except Exception as err:
                self.log('MainApps => Global communication failure: ', err)
                await asyncio.sleep(20)


gc.collect()                                                        # Очищаем RAM
def_main = MainApps()
loop = asyncio.get_event_loop()
loop.run_until_complete(def_main.main())

