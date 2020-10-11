"""Файл с настройками
   В дальнейшем здесь необходимо реализовать код 
   для сохранения пользлвательских настроек в файл 
"""

config = {}                              # Основное хранилище настроек
config['debug']          = True          # Режим отладки, вывод всех сообщений
#config['stssid']         = "GWVSOL"     # Имя точки доступа для подключения
config['stssid']         = "wSG3500"     # Имя точки доступа для подключения
#config['stpasswd']       = "fec0569cfaee" # Пароль от точки доступа
config['stpasswd']       = "Fedex##45%"  # Пароль от точки доступа
config['apssid']         = "esp8266AP"   # Имя точки доступа контроллера
config['appasswd']       = "roottoor"    # Пароль точки доступа контроллера
config['mode']           = True          # False = AP, True = ST
#config['mode']           = False        # False = AP, True = ST
config['wifiLedPin']     = 2             # Светодиод на плате подключен к 2 контакту
config['wifiLedDefault'] = 1             # Катод светодиода подключен на плюсу питания

