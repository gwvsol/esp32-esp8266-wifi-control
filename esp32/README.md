## ESP32

#### Документация  
[NodeMCU Documentation](https://nodemcu.readthedocs.io/en/dev-esp32/)  
[MicroPython documentation](https://docs.micropython.org/en/latest/index.html)  

#### Работа с сетью  
[Networking - пример использования из документации](https://docs.micropython.org/en/latest/esp32/quickref.html?highlight=net%20scan#networking)   
[network — network configuration - пример использования из документации](https://docs.micropython.org/en/latest/library/network.html?highlight=net%20scan#module-network)   
[WLAN step by step - пример использования из документации](https://docs.micropython.org/en/latest/wipy/tutorial/wlan.html?highlight=net%20scan#wlan-step-by-step)   

#### Статусы работы WiFi   
```network.STAT_BEACON_TIMEOUT```       - 200   - превышено время ответа роутера  
```network.STAT_NO_AP_FOUND```          - 201   - не удалось, потому что ни одна точка доступа не ответила  
```network.STAT_WRONG_PASSWORD```       - 202   - не удалось из-за неверного пароля  
```network.STAT_ASSOC_FAIL```           - 203   - ошибка соединения  
```network.STAT_HANDSHAKE_TIMEOUT```    - 204   - превышено время соединения  
```network.STAT_IDLE```                 - 1000  - нет связи и нет активности   
```network.STAT_CONNECTING```           - 1001  - выполняется соединение  
```network.STAT_GOT_IP```               - 1010  - соединение установлено  

#### Режимы работы   
```network.MODE_11B```                  - 1  
```network.MODE_11G```                  - 2  
```network.MODE_11N```                  - 4  