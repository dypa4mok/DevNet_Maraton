from netmiko import Netmiko
import datetime
import os

# user and password for connect
username = "devnet_user"
password = "devnet_pass"

# dir for backups
parent_dir = '/var/devnet'

# current date
now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d__%H-%M")

# devices
csr1 = {
    "host": "192.168.1.1",
    "username": username,
    "password": password,
    "device_type": "cisco_ios"}

csr2 = {
    "host": "192.168.1.2",
    "username": username,
    "password": password,
    "device_type": "cisco_ios"}

csr3 = {
    "host": "192.168.1.3",
    "username": username,
    "password": password,
    "device_type": "cisco_ios"}

"""function connect to devices, set timezone and ntp. 
    Backup config, dir name - hostname + date.
    Get from devices and output to console:
    hostname, device_type, software version, license level, CDP status, ntp status."""
for device in (csr1, csr2, csr3):
    """ connect to devices """
    connect = Netmiko(**device)

    """ configure time"""
    # configure clock timezone
    show_clock = connect.send_command("sho run | i clock")
    # example output - "clock timezone GMT 0 0"
    if not "GMT 0 0" in show_clock:
        connect.send_config_set("clock timezone GMT 0 0")

    # configure ntp
    show_ntp = connect.send_command("sho ntp config")
    # example output - " ntp server 192.168.1.10"
    if not "ntp server 192.168.1.10" in show_ntp:
        ping_ntp = connect.send_command("ping 192.168.1.10")
        if "!!!" in ping_ntp:
            connect.send_config_set("ntp server 192.168.1.10")
        else:
            print("ntp not responce " + device["host"])

    # get ntp status
    show_ntp_status = connect.send_command(
        "sho ntp status | i Clock is").split()
    # example output - "Clock is unsynchronized, stratum 16, no reference clock"
    ntp_status = "Clock is " + show_ntp_status[2].replace(',', '')

    """ get hostname and create backup """
    # get hostname
    show_hostname = connect.send_command("show runn | inc hostname").split()
    # example output - "hostname CSR_Kr_001"
    hostname = show_hostname[-1]

    # create path for backup
    dir_for_backup = os.path.join(parent_dir, today, hostname)
    if not os.path.exists(dir_for_backup):
        os.makedirs(dir_for_backup)
    # filename - hostname + date
    backup_file_path = os.path.join(
        dir_for_backup, '{}-{}.txt'.format(hostname, today))

    # get backup and write to file
    show_run = connect.send_command('show run')
    with open(backup_file_path, 'w') as file:
        file.write(show_run)

    # show cdp status
    show_cdp = connect.send_command("show cdp nei")
    if "CDP is not enabled" in show_cdp:
        cdp_status = "CDP is OFF"
    else:
        cdp_nei = connect.send_command("show cdp nei | i entries").split()
        # example output - "Total cdp entries displayed : 0"
        count_nei = cdp_nei[-1]
        cdp_status = "CDP is ON, " + count_nei + " peers"

    # sho License Level
    show_lic = connect.send_command("sho version | i License Level").split()
    # example output - "License Level: ax"
    lic_level = "lic level - " + show_lic[-1]

    # sho router model
    show_chassis = connect.send_command(
        "sho diag chassis eeprom | i PID").split()
    # exa,ple output - "Product Identifier (PID) : CSR1000V"
    device_type = show_chassis[-1]

    # sho software version
    soft_ver = connect.send_command("sho version | i Cisco IOS XE")
    # example output - "Cisco IOS XE Software, Version 16.06.05"

    # print output hostname device_type soft_ver -license level -CDP status, ntp in sync/not sync.
    print(hostname.center(10), device_type.center(10), soft_ver.center(40),
          lic_level.center(15), cdp_status.center(20), ntp_status.center(15), sep=" | ")

    # disconnetc session
    connect.disconnect()
