import gc, network
import uasyncio as asyncio

config = {}                                #Основное хранилище настроек
config['ssid'] = 'w2234'                   #SSID для подключения к WiFi
config['wf_pass'] = 'Fedex##54'            #Пароль для подключения к WiFi
config['IP'] = None                        #Дефолтный IP адрес
config['internet_outage'] = True           #Интернет отключен(значение True)

#=======================================================================
#Базовый класс
class HeatControlBase:
    DEBUG = False
    def __init__(self, config):
        self.config = config


    #Выводим отладочные сообщения
    def dprint(self, *args):
        if self.DEBUG:
            print(*args)


#=======================================================================
class HeatControl(HeatControlBase):
    def __init__(self):
        super().__init__(config)
        self._sta_if = network.WLAN(network.STA_IF)
        self.wf = self._sta_if
        
        
    #Проверка соединения с Интернетом
    asinc def check_wf(self):
        


    #Подключаемся к WiFi
    async def connect_to_WiFi(self):
        self.dprint('Connecting to WiFi...')
        self.wf.active(True)
        network.phy_mode(1) # network.phy_mode = MODE_11B
        self.wf.connect(self.config['ssid'], self.config['wf_pass'])
        if self.wf.status() == network.STAT_CONNECTING:
            self.dprint('WiFi: Waiting for connection to...')
        # Задержка на соединение, если не успешно, будет выдана одна из ошибок
        # Выполнение условия проверяем каждую секунду, задержка для получения IP адреса от DHCP
        while self.wf.status() == network.STAT_CONNECTING:
            await asyncio.sleep(1)
        #Соединение успешно установлено
        if self.wf.status() == network.STAT_GOT_IP:
            self.dprint('WiFi: Connection successful!')
            self.config['IP'] = self.wf.ifconfig()[0]
            self.dprint('WiFi:', self.config['IP'])
            self.config['internet_outage'] = False
        #Соединение не установлено...
        elif self.wf.status() == network.STAT_CONNECT_FAIL:
            self.dprint('WiFi: Failed due to other problems')
        #Соединение не установлено, причина не найдена точка доступа
        elif self.wf.status() == network.STAT_NO_AP_FOUND:
            self.dprint('WiFi: Failed because no access point replied')
        #Соединение не установлено, не верный пароль
        elif self.wf.status() == network.STAT_WRONG_PASSWORD:
            self.dprint('WiFi: Failed due to incorrect password')
