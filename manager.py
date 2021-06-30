import logging
# from eeprom.eeprom import SystemInfo
# import usb as usblib
from calendar import timegm
from time import gmtime, localtime, strftime, sleep, perf_counter
from struct import *
from threading import Thread, Lock, Event
from queue import Queue
# from linuxtools import *
# import nmea
# from utils import validate_ipv4, validate_mac, config_loggers
from copy import deepcopy
# from glcd_py.screen import *
import json
from datetime import timedelta


class Settings:
    """
    Класс для хранения настроек вебсервера
    """
    time_src = 0
    pps_src = 0
    # watchdog = 3600 * 24 * 30 * 12  # 1 year
    logger = None

    gpsd_data = {}
    eeprom = None
    # pps_sync_src = 0
    # time_sync_src = 0
    main = {
        'sync_src': '1',
        'date': 'n/a',
        'time': 'n/a',
        'timejump': '15',
        'tz': '+3',
        'tz_kv': '+0',
        'tz_rs': '+0',
        'sat_system': 'gnss',
        'ext_sync_src': 'gnss422',
        'reciever': 'irz7',
        'internal': dict(name='ГНСС внутренний',
                         speed='115200',
                         size='8',
                         parity='N',
                         stopbit='1'),
        'gnss422': dict(name='ГНСС RS-422',
                        speed='115200',
                        size='8',
                        parity='N',
                        stopbit='1'),
        'gnss232': dict(name='ГНСС RS-232',
                        speed='115200',
                        size='8',
                        parity='N',
                        stopbit='1'),
    }
    net = {
        'lan1': dict(name='lan1',
                     label='ЛВС 1',
                     ip='192.168.0.101',
                     netmask='255.255.255.0',
                     gateway='192.168.0.1',
                     status='DOWN',
                     mac='00:00:00:00:00:00',
                     listen='1',
                     speed='0'),
        'lan2': dict(name='lan2',
                     label='ЛВС 2',
                     ip='192.168.0.102',
                     netmask='255.255.255.0',
                     gateway='192.168.0.1',
                     status='DOWN',
                     mac='00:00:00:00:00:00',
                     listen='1',
                     speed='0'),
    }
    config = {
        'lifetime': 60,
        'password': '',
        'new_password': '',
        'confirm_password': '',
        'devid': '',
        'devsn': '',
        'devfd': '',
        'mcufw': '',
        'devhv': '',
        'uptime': '',
        'optime': ''
    }
    journal = [
        'all',
        'gpsd',
        'ntpd',
    ]
    header = {
        'serial': '',
        'devname': 'Часовая станция',
    }
    mcu = {
        'pps_timeout': 5,
        'connect_timeout': 1800,
        'reset_hold': 1,
        'gps_reset': 0,
        'pps_reset': 0,
        'mcu_reset': 0
    }

    def __init__(self):
        pass

    def get_config(self):
        return settings

    def save_to_file(self, func):
        return settings

    def reset(self):
        return settings

    def update(self):
        return settings


class USB:

    def __init__(self):
        self.logger = None
        self.device = None
        self.queue = Queue()
        self.lock = Lock()
        self.event = Event()
        self.handle = None

    def init(self):
        with self._lock:
            if self.device:
                del self.device
            self.device = None


class LCD:
    global settings

    def __init__(self, settings):
        self._settings = settings

    def read(self):
        return settings

    def write(self):
        return settings


settings = Settings()
lcd = LCD(settings=settings)
usb = USB()


class Manager(object):
    global settings
    global lcd
    global usb

    def __init__(self, logger):
        self.logger = logger

    def usb_reader(self):
        while True:
            if not usb.device:
                usb.init()
                continue
            packet = usb.device.read()
            response = self.unpacking(packet)
            usb.queue.put(response)

    def usb_writer(self):
        while True:
            response = usb.queue.get()
            packet = self.packing(response)
            usb.device.write(packet)

    def packing(self, response):
        packet = response
        lcd.read()
        return packet

    def unpacking(self, packet):
        response = packet
        lcd.write(response)
        return response

    def change_net_cfg(self, lan, ip, netmask, gateway, listen):
        return settings

    def get_net_cfg(self):
        return settings

    def get_main(self):
        return settings.main

    def save_time(self, date, time):
        return settings

    def save_time_settings(self, form):
        return settings

    def save_gnss(self, form):
        return settings

    def set_lifetime(self, lifetime):
        return settings

    def set_devname(self, devname):
        return settings