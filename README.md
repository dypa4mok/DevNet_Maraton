# LAB DevNet Marathon
Схема лабы:
![Схема](https://github.com/dypa4mok/DevNet_Maraton/blob/master/Lab_scheme.png)

Скрипт devnet_marathon.py запускается на сервере Ubuntu.
Скрипт выполняет следующие действия:
  - настраивает timezone GMT+0
  - настраивает ntp server
  - выполняет бэкап конфигов по пути /var/devnet/{date}/{hostname}-{date}.txt
  - собирает информацию об устройствах (hostname, device_type, software version, license level, CDP status, ntp status)
  - выводит информацию об устройствах в консоль. 

Пример вывода:
  
CSR_Kr_001 |  CSR1000V  |  Cisco IOS XE Software, Version 16.06.05  |  lic level - ax |  CDP is ON, 0 peers  | Clock is unsynchronized
CSR_Kr_002 |  CSR1000V  |  Cisco IOS XE Software, Version 16.06.05  |  lic level - ax |  CDP is ON, 0 peers  | Clock is unsynchronized
