import logging
# from eeprom.eeprom import SystemInfo
# import usb as usblib
from calendar import timegm
from time import gmtime, localtime, strftime, sleep, perf_counter
from struct import *
from threading import Thread, Lock, Event
from queue import Queue
from linuxtools import *
# import nmea
# from utils import validate_ipv4, validate_mac, config_loggers
from copy import deepcopy
from glcd_py.screen import *
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


# class LCD:
#     global settings
#
#     def __init__(self, settings):
#         self._settings = settings
#
#     def read(self):
#         return settings
#
#     def write(self):
#         return settings


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


if __name__ == '__main__':
    # lcd = StdScreen(display=None, mode=ListMode())
    # lcd.init()
    # if button & 0x0001:
    #     keys.append(event + '_left')
    # if button & 0x0002:
    #     keys.append(event + '_up')
    # if button & 0x0004:
    #     keys.append(event + '_ok')
    # if button & 0x0008:
    #     keys.append(event + '_down')
    # if button & 0x0010:
    #     keys.append(event + '_right')
    while True:
        rising = int(input())
        lcd.change_screen(rising=rising, falling=0, clamping=0, timers=0)     # right
        print()
    # lcd.change_screen(rising=0x10, falling=0, clamping=0, timers=0)     # right
    # print()
    # lcd.change_screen(rising=0x8, falling=0, clamping=0, timers=0)     # down
    # print()
    # lcd.change_screen(rising=0x4, falling=0, clamping=0, timers=0)      # ok
    # print()
    # lcd.change_screen(rising=0x2, falling=0, clamping=0, timers=0)     # down
    # print()
    # lcd.change_screen(rising=0, falling=0, clamping=1, timers=0)        # clamping left


    # for key in ('rising_ok', 'clamping_left', 'rising_sec'):
    #     time.sleep(0.5)
    #     print()
    #     print('Pressed:', key)
    #     action = lcd.action(key)
    #     print('action is', action)
    #
    #     if 'rotate' in action:
    #         if 'main' in action:
    #             # self._screenlist = deque([self._ms, self._ts, self._zs, self._ns1, self._ns2, self._gs, self._ss])
    #             print('set screen to main')
    #         elif 'left' in action:
    #             # self._screenlist.rotate(1)
    #             print('rotate left')
    #         elif 'right' in action:
    #             # self._screenlist.rotate(-1)
    #             print('rotate right')
    #         lcd = StdScreen(display=None, mode=ListMode())