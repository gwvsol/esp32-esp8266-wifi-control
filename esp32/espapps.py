import gc
import uasyncio as asyncio
from machine import Pin, freq
from espconfig import *
from esputils import dprint


class MainApps(object):

    def __init__(self):
        self.dprint      = dprint
        self.debug       = config['debug']
        self.memfree     = config['memfree']
        self.memavalable = config['memavalable']
        self.freq        = config['freq']
        self.uptime      = config['uptime']

    
    async def _run_main_loop(self):                                     #Бесконечный цикл
        while True:
            self.memfree = str(round(gc.mem_free()/1024, 2))
            self.memavalable = str(round(gc.mem_alloc()/1024, 2))
            self.freq = str(freq()/1000000)
            gc.collect()                                                #Очищаем RAM
            try:
                self.dprint('################# DEBUG MESSAGE ##########################')
                self.dprint('Uptime:', str(self.uptime)+' min')
                self.dprint('MemFree:', '{}Kb'.format(self.memfree))
                self.dprint('MemAvailab:', '{}Kb'.format(self.memavalable))
                self.dprint('FREQ:', '{}MHz'.format(self.freq))
                self.dprint('################# DEBUG MESSAGE END ######################')
            except Exception as err:
                self.dprint('Exception occurred: ', err)
            self.uptime += 1
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
