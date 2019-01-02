import gc, network
import uasyncio as asyncio
gc.collect()                                #Очищаем RAM

config = {}                                 #Основное хранилище настроек
config['MODE_WiFi'] = 'ST'
config['ssid'] = 'w2234'                    #SSID для подключения к WiFi
config['wf_pass'] = 'Fedex##54'             #Пароль для подключения к WiFi
config['IP'] = None                         #Дефолтный IP адрес
config['internet_outage'] = True            #Интернет отключен(значение True)

#=======================================================================
#Базовый класс
class WiFiBase:
    DEBUG = False
    def __init__(self, config):
        self.config = config


    #Выводим отладочные сообщения
    def dprint(self, *args):
        if self.DEBUG:
            print(*args)


    async def ping(self):
    # Проверяем есть ли соединение с интернетом
        try:
            addr = socket.getaddrinfo(self.config['host'], 80)[0][-1]
            self.dprint('Ping OK!')
            return True
        except OSError:
            self.dprint('Ping ERROR!')
            return False


    def _con(self):
        self.wf.active(True)
        network.phy_mode(1) # network.phy_mode = MODE_11B
        self.wf.connect(self.config['ssid'], self.config['wf_pass'])


    def _error_con(self):
        #Соединение не установлено...
        if self.wf.status() == network.STAT_CONNECT_FAIL:
            self.dprint('WiFi: Failed due to other problems')
        #Соединение не установлено, причина не найдена точка доступа
        if self.wf.status() == network.STAT_NO_AP_FOUND:
            self.dprint('WiFi: Failed because no access point replied')
        #Соединение не установлено, не верный пароль
        if self.wf.status() == network.STAT_WRONG_PASSWORD:
            self.dprint('WiFi: Failed due to incorrect password')


    async def connect_wf(self):
        self.dprint('Connecting to WiFi...')
        self._con()
        if self.wf.status() == network.STAT_CONNECTING:
            self.dprint('WiFi: Waiting for connection to...')
        # Задержка на соединение, если не успешно, будет выдана одна из ошибок
        # Выполнение условия проверяем каждую секунду, задержка для получения IP адреса от DHCP
        while self.wf.status() == network.STAT_CONNECTING:
            await asyncio.sleep(1)
        #Соединение успешно установлено
        if self.wf.status() == network.STAT_GOT_IP:
            self.dprint('WiFi: Connection successfully!')
            self.config['IP'] = self.wf.ifconfig()[0]
            self.dprint('WiFi:', self.config['IP'])
            self.config['internet_outage'] = False
        if not self.wf.isconnected():
            self.config['internet_outage'] = True
            self.dprint('WiFi: Connection unsuccessfully!')
        self._error_con()


    async def reconnect(self):
        self.dprint('Reconnecting to WiFi...')
        self.config['IP'] = self.wf.ifconfig()[0]
        self.wf.disconnect()
        await asyncio.sleep(1)
        self._con()
        while self.wf.status() == network.STAT_CONNECTING:
            await asyncio.sleep_ms(20)
        if self.wf.status() == network.STAT_GOT_IP:
            self.config['IP'] = self.wf.ifconfig()[0]
            self.config['internet_outage'] = False
            self.dprint('WiFi: Reconnecting successfully!')
            self.dprint('WiFi:', self.config['IP'])
        self._error_con()
        if not self.wf.isconnected():
            self.config['internet_outage'] = True
            self.dprint('WiFi: Reconnecting unsuccessfully!')
        await asyncio.sleep(1)


#=======================================================================
class WiFiControl(WiFiBase):
    def __init__(self):
        super().__init__(config)
        self._sta_if = network.WLAN(network.STA_IF)
        self.wf = self._sta_if


    #Проверка соединения с Интернетом
    async def _check_wf(self):
        while True:
            if not self.config['internet_outage']:
                if self.wf.status() == network.STAT_GOT_IP:
                    await asyncio.sleep(1)
                else:
                    await asyncio.sleep(1)
                    self.config['internet_outage'] = True
            else:
                await asyncio.sleep(1)
                await self.reconnect()
        await asyncio.sleep(1)
        gc.collect()                                   #Очищаем RAM


    #Подключаемся к WiFi
    async def connect(self):
        await self.connect_wf()
        
        loop = asyncio.get_event_loop()
        loop.create_task(self._check_wf())
