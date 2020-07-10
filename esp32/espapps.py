import gc
import uasyncio as asyncio
from machine import Pin, freq
from espconfig import *


class MainApps(object):

    def __init__(self):
        self.debug = config['debug']
    
    #Выводим отладочные сообщения
    def dprint(self, *args):
        if self.debug: print(*args)

    
    async def _run_main_loop(self):                                     #Бесконечный цикл
        while True:
            config['memfree'] = str(round(gc.mem_free()/1024, 2))
            config['memavalable'] = str(round(gc.mem_alloc()/1024, 2))
            config['freq'] = str(freq()/1000000)
            gc.collect()                                                #Очищаем RAM
            try:
                self.dprint('################# DEBUG MESSAGE ##########################')
                self.dprint('Uptime:', str(config['uptime'])+' min')
                self.dprint('MemFree:', '{}Kb'.format(config['memfree']))
                self.dprint('MemAvailab:', '{}Kb'.format(config['memavalable']))
                self.dprint('FREQ:', '{}MHz'.format(config['freq']))
                self.dprint('################# DEBUG MESSAGE END ######################')
            except Exception as err:
                self.dprint('Exception occurred: ', err)
            config['uptime'] += 1
            await asyncio.sleep(60)


    async def main(self):
        while True:
            try:
                await self._run_main_loop()
            except Exception as err:
                self.dprint('Global communication failure: ', err)
                await asyncio.sleep(20)


gc.collect()                                            #Очищаем RAM
def_main = MainApps()
loop = asyncio.get_event_loop()
loop.run_until_complete(def_main.main())
