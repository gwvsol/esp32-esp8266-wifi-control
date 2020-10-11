import gc
import uasyncio as asyncio
from machine import Pin, freq
from espconfig import *
from esputils import dprint
from espwlan import WiFiConnect

"""Здесь реализуется основное приложение
   подключена работа wifi модуля и его управление 
   а так же вывод основной информации о работе микроконтроллера"""

class MainApps(object):

    def __init__(self):
        self.dprint          = dprint
        self.debug           = config['debug']
        self.mode            = config['mode']
        self.ledBoard        = config['wifiLedPin']
        self.ledBoardDefault = config['wifiLedDefault']
        self.uptime          = 0                                   # Время работы контроллера
        self.wifiLed         = Pin(self.ledBoard, Pin.OUT, value = self.ledBoardDefault) # Cветодиод для индикации работы WiFi
        self.wifi            = WiFiConnect(led=self.wifiLed)       # Настрока сети
    
    async def main_loop(self):
        """Метод для вывода служебной отладочной информации"""
        while True:                                                # Бесконечный цикл
            self.ip          = self.wifi.ip                        # IP адрес полученный c DHCP роутера
            self.connect     = self.wifi.connect                   # False = Подключения нет, True = Подключение к сети WiFi
            self.memfree = str(round(gc.mem_free()/1024, 2))       # Свободная память
            self.memavalable = str(round(gc.mem_alloc()/1024, 2))  # Доступная помять
            self.freq = str(freq()/1000000)                        # Частота работы ядра процессора
            mode = 'Station' if self.mode else 'Access Point'      # Подготовка информации о режиме работы WiFi модуля
            connect = 'Connect' if self.connect else 'Disconnect'  # Подготовка информации о соединении
            gc.collect()                                           # Очищаем RAM
            try:
                self.dprint('################# DEBUG MESSAGE ##########################')
                self.dprint('Uptime:', str(self.uptime)+' min')
                self.dprint('MemFree:', '{}Kb'.format(self.memfree))
                self.dprint('MemAvailab:', '{}Kb'.format(self.memavalable))
                self.dprint('FREQ:', '{}MHz'.format(self.freq))
                self.dprint('WiFi Mode:', mode)
                self.dprint('WiFi:', connect)
                self.dprint('IP:', '{}'.format(self.ip))
                self.dprint('################# DEBUG MESSAGE END ######################')
            except Exception as err:
                self.dprint('Exception occurred: ', err)
            self.uptime += 1
            await asyncio.sleep(60)


    async def main(self):
        while True:
            try:
                await self.wifi.setWlan()                           # Включение настройки сети
                await self.main_loop()                              # Вывод служебной информации
            except Exception as err:
                self.dprint('Global communication failure: ', err)
                await asyncio.sleep(20)


gc.collect()                                                        # Очищаем RAM
def_main = MainApps()
loop = asyncio.get_event_loop()
loop.run_until_complete(def_main.main())
