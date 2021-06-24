from threading import Thread, Lock, Event
from queue import Queue
from flask import Flask
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_socketio import SocketIO

from auth import User, CustomLoginManager


class Settings:
    def __init__(self):
        pass

    def get_config(self):
        return settings

    def save_to_file(self, func):
        return settings

    def reset_settings(self):
        return settings

    def save_settings(self):
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
        return settings

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


settings = Settings()
lcd = LCD(settings=settings)
usb = USB()

app = Flask(__name__)
socketio = SocketIO(app, async_mode=None, cookie=None, logger=False, engineio_logger=False)
manager = Manager(app.logger)

user = User(1, u"name")
login_manager = CustomLoginManager()
login_manager.init(app)


if __name__ == '__main__':
    login_user(user)
    print(current_user.is_authenticated)
    socketio.run(app, debug=False, host='0.0.0.0', port='5001')
