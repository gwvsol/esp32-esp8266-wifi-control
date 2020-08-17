import gc, network
import uasyncio as asyncio
from machine import Pin
from espconfig import *
from esputils import dprint
gc.collect()                                #Очищаем RAM

"""Класс реализующий подключение в точке доступа 
   или же поднятие точки доступа на WiFi модуле микроконтроллера"""

class WiFiConnect(object):

    def __init__(self, led=None):
        self.dprint     = dprint                # Метод для логирования работы
        self.mode       = config['mode']        # False = AP, True = ST
        self.debug      = config['debug']       # True = Режим отладки, вывод всех сообщений через dprint
        self.connect    = False                 # False = Подключения нет, True = Подключение к сети WiFi
        self.ip         = "0.0.0.0"             # IP адрес
        self.led        = led                   # Если настройки светодиода не будут переданы, индикация не будет включена
        self.loop = asyncio.get_event_loop()
        if isinstance(self.led, Pin):
            # Управление в отдельном процессе запускается только 
            # если классу переданы настройки для работы светодиода
            self.loop.create_task(self.controlHeartbeat())

############### Методы индикации состояния WiFi модуля микроконтроллера ###############

    async def heartbeat(self, interval: list=[1000]):
        """Метод для индикации работы WiFi"""
        # Мигание согласно переданной программе (спикок интервалов)
        for i in interval:
            self.led(not self.led())
            await asyncio.sleep_ms(i)

    
    async def setHeartbeatDefault(self):
       """Метод для начальной уставноки состояния светодиода"""
       # Работает только если классу переданы настройки светодиода
       if isinstance(self.led, Pin): self.led(0)
            
    
    async def controlHeartbeat(self):
        """Метод для управления работой работой светодиода wifi"""
        while True:
            # Одно короткое мигание и длинная пауза при успешном подключении к точке доступа
            if self.mode and self.connect: await self.heartbeat(interval=[100, 5000])
            # Быстрое мигание при отсутствии подключения
            elif self.mode and not self.connect: await self.heartbeat(interval=[200])
            # Длинная пауза и три быстрых мигания при поднятой точке доступа на микроконтроллере
            elif not self.mode: await self.heartbeat(interval=[5000, 100, 100, 100])
                
################## Методы для управления WiFi модулем микроконтроллера ###################

    # Настройка WiFi подключение к сети или поднятие точки доступа (этот метод необходимо вызвать для
    # поднятия точки доступа или подключения к точке доступа)
    async def setWlan(self):
        """Метод для активации режимов работы WiFi модуля"""
        # Подключение к сети
        if self.mode: 
            self.wifi, self.ssid, self.passwd = \
            network.WLAN(network.STA_IF), config['stssid'], config['stpasswd']   # ST Mode
            network.phy_mode(network.MODE_11B)                                   # network.phy_mode = MODE_11B
        # Поднимаем точку доступа
        elif not self.mode: self.wifi, self.ssid, self.passwd = \
            network.WLAN(network.AP_IF), config['apssid'], config['appasswd']    # AP Mode
        self.wifi.active(True)                                                   # Активигуем интерфейс
        if self.mode: 
            await self.setSTMode()
            # В режиме ST Mode запускаем в отдельном процессе контроль wifi соединения
            self.loop.create_task(self.checkWiFiStatus())
        else: await self.setAPMode()
    

    async def checkWiFiStatus(self):
        """Метод для проверки наличия соединения с точкой тоступа WiFi, 
           и вывода статуса соединения или режима работы (ST Mode или AP Mode)"""
           # Этот метод крутится в отдельном процессе для контроля соединения
        while True:
            # При наличии соединения
            if self.mode and self.connect:
                if await self.statusConnect() == network.STAT_GOT_IP:
                    await asyncio.sleep(30)     # Засыпаем
                else: 
                    self.connect = False        # Cоединение отсутствует
                    await asyncio.sleep(1)      # Засыпаем
            # При отсутствии соединения
            elif self.mode and not self.connect:
                await self.reconnectWifi()      # Переподключаемся
                await asyncio.sleep(5)          # Засыпаем
            gc.collect()


    async def reconnectWifi(self):
        """Метод для переподключения к точке доступа WiFi"""
        self.dprint('Reconnecting to WiFi...')
        self.ip = self.wifi.ifconfig()[0]   # Сбрасываем IP адрес к виду 0.0.0.0
        self.wifi.disconnect()              # Разрываем соединение, если они не разорвано
        await asyncio.sleep(1)              # Ожидаем
        await self.setSTMode()              # Пробуем повторно подключиться


    async def setSTMode(self):
        """Метод для подключения к точке доступа"""
        if not self.wifi.isconnected():
            self.wifi.connect(self.ssid, self.passwd)
        count = 0 # Счетчик попыток подключения
        # Ожидаем подключения
        while await self.statusConnect() == network.STAT_CONNECTING:
            await asyncio.sleep(1)
            count += 1
            if count == 10: break                # Если счетчик переполнился, выходим из цикла
        # Если соединение установлено
        if self.wifi.isconnected():
            await self.setHeartbeatDefault()     # Сбрасываем состояние светодиода в дефолт
            self.ip = self.wifi.ifconfig()[0]
            self.dprint('WiFi: Connection successfully!')
            self.connect = True                  # Cоединение установлено
            self.dprint('WiFi: Address', self.ip)
        # Если соединение не установлено
        if not self.wifi.isconnected():
            self.connect = False                 # Cоединение не установлено
            self.dprint('WiFi: Connection unsuccessfully!')

    
    async def statusConnect(self):
        """Метод для вывода информации о статусе соединения"""
        status = self.wifi.status()
        if status == network.STAT_GOT_IP:               # Соединение установлено
            self.dprint('WiFi: Connect OK')
            return network.STAT_GOT_IP
        elif status == network.STAT_CONNECTING:         # В процессе соединения...
            self.dprint('WiFi: Connecting to WiFi...')
            return network.STAT_CONNECTING
        elif status == network.STAT_ASSOC_FAIL:         # Ошибка соединения
            self.dprint('WiFi: Connection error')
            return network.STAT_ASSOC_FAIL
        elif status == network.STAT_HANDSHAKE_TIMEOUT:  # Превышено время соединения
            self.dprint('WiFi: Connection time exceeded')
            return network.STAT_HANDSHAKE_TIMEOUT
        elif status == network.STAT_BEACON_TIMEOUT:     # Превышено время ответа роутера
            self.dprint('WiFi: Exceeded response time of the router')
            return network.STAT_BEACON_TIMEOUT
        elif status == network.STAT_NO_AP_FOUND:        # Ни одна точка доступа не ответила
            self.dprint('WiFi: None the access point did not answer')
            return network.STAT_NO_AP_FOUND
        elif status == network.STAT_WRONG_PASSWORD:     # Соединение не установлено, не верный пароль
            self.dprint('WiFi: Failed due to incorrect password')
            return network.STAT_WRONG_PASSWORD
        elif status == network.STAT_IDLE:               # Соединение отсуствует, нет активности
            self.dprint('WiFi: Idle state, no connection, and no activity')
            return network.STAT_IDLE
        else: # Любые другие варианты статусов, вывод в лог
            self.dprint('WiFi: Status', status)
            return status


    async def setAPMode(self):
        """Метод для включения на миктрокотроллере режима точки доступа"""
        #Устанавливаем SSID и пароль для подключения к Точке доступа
        self.wifi.config(essid=self.ssid)       # SSID точки доступа
        self.wifi.config(password=self.passwd)  # Пароль точки доступа
        self.wifi.config(max_clients=5)         # Максимальное количество клиентов для подключения
        self.wifi.config(channel=11)            # Канал точки доступа
        self.wifi.config(authmode=3)            # Способ аунтентиикации 0 – open, 1 – WEP, 2 – WPA-PSK, 3 – WPA2-PSK, 4 – WPA/WPA2-PSK 
        self.ip = self.wifi.ifconfig()[0]       # Выводим IP адрес точки доступа
        await self.setHeartbeatDefault()        # Сбрасываем состояние светодиода в дефолт

