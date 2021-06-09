settings = {}
# unpack_queue = None
# pack_queue = None
# usbtx_queue = None
# usbrx_queue = None
manager_queue = None
usb_queue = None
lcd_queue = None


class USB:

    def __init__(self, logger):
        self.device = None
        self.queue = None
        self._lock = Lock()
        self.event = Event()
        self.logger = logger
        self.init()

    def init(self):
        with self._lock:
            if self.device:
                del self.device
            self.device = None


class LCD:
    global settings

    def read(self):
        return settings

    def write(self):
        return settings


class Manager:
    global settings
    global lcd
    global usb

    def __init__(self):
        # self.lcd = LCD()
        # self.usb = USB()
        pass

    def reader_thread(self):
        while True:
            if not usb.device:
                usb.init()
                continue
            packet = usb.device.read()
            response = self.unpacking(packet)
            usb.queue.put(response)

    def writer_thread(self):
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

    def reset_settings(self):
        return settings

    def save_settings(self):
        return settings

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

    def get_config(self):
        return settings


if __name__ == '__main__':
    lcd = LCD()
    usb = USB()
    manager = Manager()
