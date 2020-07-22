config = {}                             # Основное хранилище настроек
config['debug']         = True          # Режим отладки, вывод всех сообщений
config['stssid']        = "wSG3500"     # Имя точки доступа для подключения
config['stpasswd']      = "Fedex##45%"  # Пароль от точки доступа
config['apssid']        = "esp32AP"     # Имя точки доступа контроллера
config['appasswd']      = "roottoor"    # Пароль точки доступа контроллера
config['ip']            = "xxx.xxx.xxx.xxx" # IP адрес полученный c DHCP роутера
config['uptime']        = 0             # Время работы контроллера
config['memfree']       = 0             # Свободная память
config['memavalable']   = 0             # Доступная помять
config['freq']          = 0             # Частота работы ядра процессора
config['connect']       = False         # False = Подключения нет, True = Подключение к сети WiFi
config['mode']          = False         # False = AP, True = ST

