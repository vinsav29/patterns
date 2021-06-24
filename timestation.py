from threading import Thread, Lock, Event
from queue import Queue
from flask import Flask, render_template, session, request, \
    redirect, url_for, flash, jsonify
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

flask_app = Flask(__name__)
socketio = SocketIO(flask_app, async_mode=None, cookie=None, logger=False, engineio_logger=False)
manager = Manager(flask_app.logger)

user = User(1, u"name")
login_manager = CustomLoginManager()
login_manager.init(flask_app)


@flask_app.route("/login.html", methods=["GET", "POST"])
def login():
    return render_template("login.html", header=settings.header)


@flask_app.route("/logout", methods=["GET", "POST"])
# @authenticated_only
def logout():
    user.logout()
    # flash_message("Выход из системы!", 'warning')
    return redirect(url_for("login"))


@flask_app.route("/reauth", methods=["POST"])
def reauth():
    data = {}
    msg = request.form.get("msg")
    manager.logger.debug(msg)
    manager.logger.error('Смена пароля...')
    # if msg == 'not_equal_passwords':
    #     flash_message(u"Новые пароли не совпадают!", 'warning')
    # elif msg == 'null_password':
    #     flash_message(u"Не введен новый пароль!", 'warning')
    # elif msg:
    #     data['pass_verify'] = user.check_password(request.form["msg"])
    #     if not data['pass_verify']:
    #         flash_message(u"Неверный пароль!", 'warning')
    #     else:
    #         flash_message(u"Пароль изменен!")
    return jsonify(data)


if __name__ == '__main__':
    login_user(user)
    print(current_user.is_authenticated)
    socketio.run(flask_app, debug=False, host='0.0.0.0', port='5001')
