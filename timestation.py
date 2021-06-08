settings = {}
# unpack_queue = None
# pack_queue = None
# usbtx_queue = None
# usbrx_queue = None
manager_queue = None
usb_queue = None
lcd_queue = None

class USB:
    global settings
    global manager

    def usb_init(self):
        return settings

    def usb_reader(self, usb_queue, usb_lock):
        while True:
            packet = usb.read()
            manager_queue.put(packet)
            # response = manager.unpacking(packet)
            # usb_queue.put(response)

    def usb_writer(self, usb_queue, usb_lock):
        while True:
            response = usb_queue.get()
            manager_queue.put(packet)
            # packet = manager.packing(response)
            usb.write(packet)



class LCD:
    global settings

    def read(self):
        return settings

    def write(self):
        return settings


class Manager:
    global settings

    def __init__(self):
        lcd = LCD()
        # usb = USB()

    # def usb_init(self):
    #     return settings
    #
    # def usb_reader(self, usb_queue, usb_lock):
    #     while True:
    #         packet = usb.read()
    #         response = self.unpacking(packet)
    #         usb_queue.put(response)
    #
    # def usb_writer(self, usb_queue, usb_lock):
    #     while True:
    #         response = usb_queue.get()
    #         packet = self.packing(response)
    #         usb.write(packet)

    def packing_thread(self):
        while True:

            usb_queue.put(response)

    def unpacking_thread(self):
        while True:
            packet = manager_queue.get()
            response = unpack(packet)

            lcd_queue.put(response)

    # def packing(self, name='void'):
    #     packet = pack(response)
    #     lcd.read()
    #     return packet
    #
    # def unpacking(self):
    #     response = unpack(packet)
    #     lcd.write(response)
    #     return response

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
