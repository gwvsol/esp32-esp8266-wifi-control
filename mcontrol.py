import gc
import uasyncio as asyncio
from machine import Pin
from wificonnect import WiFiControl

#=======================================================================
class Main(WiFiControl):
    def __init__(self):
        super().__init__()
        self.DEBUG = True                               #Режим отладки, делаем программу разговорчивой
        self.wifi_led = Pin(2, Pin.OUT, value = 1)      #Pin2, светодиод на плате контроллера

        loop = asyncio.get_event_loop()
        loop.create_task(self._heartbeat())             #Индикация подключения WiFi
    
    #Индикация подключения WiFi
    async def _heartbeat(self):
        while True:
            if self.config['internet_outage']:
                self.wifi_led(not self.wifi_led())      #Быстрое мигание, если соединение отсутствует
                await asyncio.sleep_ms(200) 
            else:
                self.wifi_led(0)                        #Редкое мигание при подключении
                await asyncio.sleep_ms(50)
                self.wifi_led(1)
                await asyncio.sleep_ms(5000)


    async def _run_main_loop(self):                     #Бесконечный цикл
        mins = 0
        while True:
            gc.collect()                                #Очищаем RAM
            try:
                self.dprint('Uptime:', str(mins)+' min')
                self.dprint('Not WiFi:', self.config['internet_outage'])
                self.dprint('IP:', self.config['IP'])
                self.dprint('MemFree:', str(round(gc.mem_free()/1024, 2))+' Kb')
                self.dprint('MemAlloc:', str(round(gc.mem_alloc()/1024, 2))+' Kb')
            except Exception as e:
                self.dprint('Exception occurred: ', e)
            mins += 1
            await asyncio.sleep(60)


    async def main(self):
        while True:
            try:
                await self.connect()
                await self._run_main_loop()
            except Exception as e:
                self.dprint('Global communication failure: ', e)
                await asyncio.sleep(20)


gc.collect()                                            #Очищаем RAM
def_main = Main()
loop = asyncio.get_event_loop()
loop.run_until_complete(def_main.main())
