from datetime import datetime
import time
# import struct
from struct import pack
from collections import deque

from .glcdlib import *
from .stdscreen import *

from .font.font_terminus12m import *
from .font.font_terminus18m import *

import linuxtools


class MainScreen(StdScreen):
    _sats = 0
    _time_src = ''
    _pps_src = ''

    def __init__(self, display, label, settings):
        self.label = label
        self._settings = settings

        StdScreen.__init__(self, display)

    def refresh_data(self):
        print(f"{type(self).__name__} refresh_data")
        sats = self._settings.gpsd_data.get('sats_valid')
        if isinstance(sats, int):
            self._sats = sats
        else:
            self._sats = 0

        time_src = self._settings.time_src
        if time_src == linuxtools.TIME_SRC_INTERNAL:
            self._time_src = 'Внтр'
        elif time_src == linuxtools.TIME_SRC_GNSS:
            self._time_src = 'ГНСС'
        else:
            self._time_src = 'Нет'

        pps_src = self._settings.pps_src
        if pps_src == linuxtools.PPS_SRC_INTERNAL:
            self._pps_src = 'Внтр'
        elif pps_src == linuxtools.PPS_SRC_GNSS:
            self._pps_src = 'ГНСС'
        else:
            self._pps_src = 'Нет'

        tm = time.localtime()

        self.strings = [
            time.strftime("%T", tm),
            time.strftime("%d.%m.%y", tm),
            'Спутн:{:d}'.format(self._sats),
            'Время:{:s}'.format(self._time_src),
            'Синхр:{:s}'.format(self._pps_src)]

    # def EnterListMode(self):
    #     print(f"{type(self).__name__} EnterListMode")
    #     self.refresh_data()
    #     tm = time.localtime()
    #
    #     self.strings = [
    #         time.strftime("%T", tm),
    #         time.strftime("%d.%m.%y", tm),
    #         'Спутн:{:d}'.format(self._sats),
    #         'Время:{:s}'.format(self._time_src),
    #         'Синхр:{:s}'.format(self._pps_src)]
    #
    #     self.Draw()
        # StdScreen.EnterListMode(self, strings)
    #
    # def EnterEditMode(self):
    #     return
    #
    # def ExitEditMode(self):
    #     return

    def draw(self):
        print(f"{type(self).__name__} draw")
        print(self.strings)

        self.GLCD.Clear()

        self.GLCD.SetFont(Terminus18m)
        self.GLCD.DrawString(0, 0, self.strings[0])
        self.GLCD.DrawString(0, 15, self.strings[1])

        self.GLCD.SetFont(Terminus12m)
        self.GLCD.DrawString(64, 0, self.strings[2])
        self.GLCD.DrawString(64, 11, self.strings[3])
        self.GLCD.DrawString(64, 22, self.strings[4])


class TimeScreen(StdScreen):

    def __init__(self, display, label, settings):
        self.label = label
        self._settings = settings
        StdScreen.__init__(self, display)

        editor_strings = [
            'Время: [d00]:[d00]:[d00]',
            'Дата: [d00].[d00].[d00]'
        ]

        self.CreateEditorMap(editor_strings)

    def refresh_data(self, *args):
        print(f"{type(self).__name__} refresh_data")

        tm = time.localtime()

        self.strings = [
            time.strftime("Время: %T", tm),
            time.strftime("Дата: %d.%m.%y", tm),
        ]

    def ExitEditMode(self):
        print(f"{type(self).__name__} ExitEditMode")

        sync_src = int(self._settings.main['sync_src'])
        if sync_src != linuxtools.GNSS_SRC_NONE:
            message = [
                'Не установлено!',
                'Измените источник',
                'синхронизации на:',
                linuxtools.sync_sources[linuxtools.GNSS_SRC_NONE]
            ]
            StdScreen.EnterMessageMode(self, message)
            return False

        params = self.GetEditorParams()
        print(params)

        errors = []
        try:
            datetime.strptime(':'.join(params[0]), '%H:%M:%S')
        except ValueError:
            errors.append('Время')
        try:
            datetime.strptime('.'.join(params[1]), '%d.%m.%y')
        except ValueError:
            errors.append('Дата')

        if not errors:
            # StdScreen.ExitEditMode(self)
            return True
        else:
            message = ['Неверный параметр'] + errors
            StdScreen.EnterMessageMode(self, message)
            return False


class ZoneScreen(StdScreen):
    _tz = 3
    _tz_kv = 0
    _tz_rs = 0

    def __init__(self, display, label, settings):
        self.label = label
        self._settings = settings
        StdScreen.__init__(self, display)

        editor_strings = [
            'Станция: [d+00]',
            'Табло КВ: [d+00]',
            'Табло RS: [d+00]'
        ]

        self.CreateEditorMap(editor_strings)

    def refresh_data(self):
        print(f"{type(self).__name__} refresh_data")

        tm = time.localtime()
        self._tz = int(time.strftime("%z", tm)[:-2])
        self._tz_kv = int(self._settings.main['tz_kv'])
        self._tz_rs = int(self._settings.main['tz_rs'])

        self.strings = [
            'Станция: {:+03d}'.format(self._tz),
            'Табло КВ: {:+03d}'.format(self._tz_kv),
            'Табло RS: {:+03d}'.format(self._tz_rs)
        ]

    # def EnterListMode(self):
    #     self.refresh_data()
    #
    #     strings = [
    #         'Станция: {:+}'.format(self._tz),
    #         'Табло КВ: {:+}'.format(self._tz_kv),
    #         'Табло RS: {:+}'.format(self._tz_rs)
    #     ]
    #
    #     StdScreen.EnterListMode(self, strings)

    # def EnterEditMode(self):
    #     self.refresh_data()
    #
    #     self.strings = [
    #         'Станция: [d{:+03d}]'.format(self._tz),
    #         'Табло КВ: [d{:+03d}]'.format(self._tz_kv),
    #         'Табло RS: [d{:+03d}]'.format(self._tz_rs)
    #     ]
    #
    #     StdScreen.EnterEditMode(self)

    def ExitEditMode(self):

        (tz,), (tz_kv,), (tz_rs,) = self.GetEditorParams()

        errors = []
        if not -12 <= int(tz) <= 14:
            errors.append('Станция')
        if not -12 <= int(tz_kv) <= 14:
            errors.append('Табло КВ')
        if not -12 <= int(tz_rs) <= 14:
            errors.append('Табло RS')

        if not errors:
            StdScreen.ExitEditMode(self)
            return True
        else:
            strings = ['Неверный параметр'] + errors
            StdScreen.EnterMessageMode(self, strings)
            return False


class NetScreen(StdScreen):
    _ip = None
    _sn = None
    _gw = None
    _hw = None
    _status = None
    _ntp = None

    def __init__(self, display, label, lan, settings):
        self.label = label
        self._lan = lan
        self._settings = settings
        StdScreen.__init__(self, display)

        editor_strings = [
            'IP: [d000].[d000].[d000].[d000]',
            'SN: [d000].[d000].[d000].[d000]',
            'GW: [d000].[d000].[d000].[d000]',
            'HW: AB:BC:CD:DE:EF:F0',
            'NTP: [bS]'
        ]

        self.CreateEditorMap(editor_strings)

    def refresh_data(self):
        lan = self._lan
        self._ip = self._settings.net[lan]['ip']
        self._sn = self._settings.net[lan]['netmask']
        self._gw = self._settings.net[lan]['gateway']
        self._hw = self._settings.net[lan]['mac']
        self._ntp = self._settings.net[lan]['listen']

        ip = self._ip.split('.')
        sn = self._sn.split('.')
        gw = self._gw.split('.')

        if self._ntp == '1':
            ntp = CP_YES
        else:
            ntp = CP_NO

        self.strings = [
            'IP: {:>03s}.{:>03s}.{:>03s}.{:>03s}'.format(*ip),
            'SN: {:>03s}.{:>03s}.{:>03s}.{:>03s}'.format(*sn),
            'GW: {:>03s}.{:>03s}.{:>03s}.{:>03s}'.format(*gw),
            'HW: {:s}'.format(self._hw),
            'NTP: {:s}'.format(ntp)
        ]

    # def EnterListMode(self):
    #     self.refresh_data()
    #     if self._ntp == '1':
    #         ntp = CP_YES
    #     else:
    #         ntp = CP_NO
    #     strings = [
    #         'IP: {:s}'.format(self._ip),
    #         'SN: {:s}'.format(self._sn),
    #         'GW: {:s}'.format(self._gw),
    #         'HW: {:s}'.format(self._hw),
    #         'NTP: {:s}'.format(ntp)
    #     ]
    #     StdScreen.EnterListMode(self, strings)

    # def EnterEditMode(self):
    #     self.refresh_data()
    #     ip = self._ip.split('.')
    #     sn = self._sn.split('.')
    #     gw = self._gw.split('.')
    #     if self._ntp == '1':
    #         ntp = CP_YES
    #     else:
    #         ntp = CP_NO
    #
    #     ip = 'IP: [d{:>03s}].[d{:>03s}].[d{:>03s}].[d{:>03s}]'.format(*ip)
    #     sn = 'SN: [d{:>03s}].[d{:>03s}].[d{:>03s}].[d{:>03s}]'.format(*sn)
    #     gw = 'GW: [d{:>03s}].[d{:>03s}].[d{:>03s}].[d{:>03s}]'.format(*gw)
    #     hw = 'HW: {:s}'.format(self._hw)
    #     ntp = 'NTP: [b{:s}]'.format(ntp)
    #
    #     strings = [ip, sn, gw, hw, ntp]
    #     StdScreen.EnterEditMode(self, strings)

    def ExitEditMode(self):
        params = self.GetEditorParams()

        ip, sn, gw, _, ntp = params

        errors = []
        from utils import validate_ipv4
        if not validate_ipv4('.'.join(ip)):
            errors.append('IP')
        if not validate_ipv4('.'.join(sn)):
            errors.append('SN')
        if not validate_ipv4('.'.join(gw)):
            errors.append('GW')

        if not errors:
            StdScreen.ExitEditMode(self)
            return True
        else:
            strings = ['Неверный параметр'] + errors
            StdScreen.EnterMessageMode(self, strings)
            return False


class GnssScreen(StdScreen):
    _time = ''
    _date = ''
    _latitude = ''
    _longitude = ''
    _speed = ''
    _altitude = ''
    _sats = ''
    _sats_valid = ''
    _status = ''

    def __init__(self, display, label, settings):
        self.label = label
        self._settings = settings
        StdScreen.__init__(self, display)

    def refresh_data(self):
        mode = self._settings.gpsd_data.get('mode')
        if mode is None:
            mode = -1
        if mode >= 0:
            if self._settings.gpsd_data.get('sats'):
                self._sats = str(self._settings.gpsd_data.get('sats'))
            if self._settings.gpsd_data.get('sats_valid'):
                self._sats_valid = str(self._settings.gpsd_data.get('sats_valid'))

            if self._settings.gpsd_data.get('status') == 1:
                self._status = 'верно'
            elif self._settings.gpsd_data.get('status') == 0:
                self._status = 'не верно'
            else:
                self._status = 'нет данных'
            self._time = self._settings.gpsd_data['time']
            self._date = self._settings.gpsd_data['date']
            self._latitude = self._settings.gpsd_data['latitude']
            self._longitude = self._settings.gpsd_data['longitude']
            self._speed = str(self._settings.gpsd_data['speed'])
            self._altitude = str(self._settings.gpsd_data['altitude'])
        else:
            self._time = '-'
            self._date = '-'
            self._latitude = '-'
            self._longitude = '-'
            self._speed = '-'
            self._altitude = '-'
            self._sats = '-'
            self._sats_valid = '-'
            self._status = 'нет данных'

    def EnterListMode(self):
        self.refresh_data()
        strings = [
            'Статус: {:s}'.format(self._status),
            'Вид. cпутники: {:s}'.format(self._sats),
            'Исп. cпутники: {:s}'.format(self._sats_valid),
            'Время: {:s}'.format(self._time),
            'Дата: {:s}'.format(self._date),
            'Широта: ' + '{:s}'.format(self._latitude).replace(' ', ''),
            'Долгота: ' + '{:s}'.format(self._longitude).replace(' ', ''),
            'Скорость,м/с: {:s}'.format(self._speed),
            'Высота,м: {:s}'.format(self._altitude),
        ]
        StdScreen.EnterListMode(self, strings)

    def EnterEditMode(self):
        # self.refresh_data()
        # ip = self._ip.split('.')
        # sn = self._sn.split('.')
        # gw = self._gw.split('.')
        #
        # ip = 'IP: [d{:>03s}].[d{:>03s}].[d{:>03s}].[d{:>03s}]'.format(*ip)
        # sn = 'SN: [d{:>03s}].[d{:>03s}].[d{:>03s}].[d{:>03s}]'.format(*sn)
        # gw = 'GW: [d{:>03s}].[d{:>03s}].[d{:>03s}].[d{:>03s}]'.format(*gw)
        # hw = 'HW: {:s}'.format(self._hw)
        # ntp = 'NTP: [d{:s}]'.format(self._ntp)
        #
        # strings = [ip, sn, gw, hw, ntp]
        # StdScreen.EnterEditMode(self, strings)
        pass

    def ExitEditMode(self):
        # params = self.GetEditorParams()
        #
        # ip, sn, gw, _, ntp = params
        #
        # errors = []
        # from utils import validate_ipv4
        # if not validate_ipv4('.'.join(ip)):
        #     errors.append('IP')
        # if not validate_ipv4('.'.join(sn)):
        #     errors.append('SN')
        # if not validate_ipv4('.'.join(gw)):
        #     errors.append('GW')
        #
        # if not errors:
        #     StdScreen.ExitEditMode(self)
        #     return True
        # else:
        #     strings = ['Неверный параметр'] + errors
        #     StdScreen.EnterMessageMode(self, strings)
        #     return False
        pass


class SyncScreen(StdScreen):

    def __init__(self, display, label, settings):
        self.label = label
        self._settings = settings
        StdScreen.__init__(self, display)

    def refresh_data(self):
        pass

    def EnterListMode(self):
        self.refresh_data()

        strings = [
            'Ист. синхр: {:s}'.format('внутр.'),
            'Ист. ГНСС: {:s}'.format('внутр.'),
            'Система ГНСС: {:s}'.format('общ.')
        ]
        StdScreen.EnterListMode(self, strings)

    # def EnterEditMode(self):
    #     self.refresh_data()
    #     ip = self._ip.split('.')
    #     sn = self._sn.split('.')
    #     gw = self._gw.split('.')
    #     if self._ntp == '1':
    #         ntp = CP_YES
    #     else:
    #         ntp = CP_NO
    #
    #     ip = 'IP: [d{:>03s}].[d{:>03s}].[d{:>03s}].[d{:>03s}]'.format(*ip)
    #     sn = 'SN: [d{:>03s}].[d{:>03s}].[d{:>03s}].[d{:>03s}]'.format(*sn)
    #     gw = 'GW: [d{:>03s}].[d{:>03s}].[d{:>03s}].[d{:>03s}]'.format(*gw)
    #     hw = 'HW: {:s}'.format(self._hw)
    #     ntp = 'NTP: [b{:s}]'.format(ntp)
    #
    #     strings = [ip, sn, gw, hw, ntp]
    #     StdScreen.EnterEditMode(self, strings)
    #
    # def ExitEditMode(self):
    #     params = self.GetEditorParams()
    #
    #     ip, sn, gw, _, ntp = params
    #
    #     errors = []
    #     from utils import validate_ipv4
    #     if not validate_ipv4('.'.join(ip)):
    #         errors.append('IP')
    #     if not validate_ipv4('.'.join(sn)):
    #         errors.append('SN')
    #     if not validate_ipv4('.'.join(gw)):
    #         errors.append('GW')
    #
    #     if not errors:
    #         StdScreen.ExitEditMode(self)
    #         return True
    #     else:
    #         strings = ['Неверный параметр'] + errors
    #         StdScreen.EnterMessageMode(self, strings)
    #         return False


class LCD:
    def __init__(self, settings) -> None:
        self._display = Display()
        self._screenlist = deque()
        self._ms = MainScreen(self._display, label='Главный экран', settings=settings)
        self._ts = TimeScreen(self._display, label='Дата и время', settings=settings)
        self._zs = ZoneScreen(self._display, label='Часовые пояса', settings=settings)
        self._ns1 = NetScreen(self._display, label='ЛВС 1', lan='lan1', settings=settings)
        self._ns2 = NetScreen(self._display, label='ЛВС 2', lan='lan2', settings=settings)
        self._gs = GnssScreen(self._display, label='Приёмник ГНСС', settings=settings)
        self._ss = SyncScreen(self._display, label='Синхронизация', settings=settings)

        self._screenlist = deque([self._ms, self._ts, self._zs, self._ns1, self._ns2, self._gs, self._ss])

        self.MainScreenObject = self._ms
        self.CurrentScreenObject = self._ms
        self.CurrentScreenObject.init()
        self.CurrentScreenObject.draw()

        self._settings = settings

    def show_screen(self):
        return self._display.Screen

    def change_screen(self, rising=0, falling=0, clamping=0, timers=0):
        keys = []
        self.btn_naming(keys, 'rising', rising)
        self.btn_naming(keys, 'falling', falling)
        self.btn_naming(keys, 'clamping', clamping)

        if timers & 0x0008:
            keys.append('rising_sec')

        if keys:
            action = self.CurrentScreenObject.action(keys)
            print('ACTION:', action)
            if action:
                if 'rotate' in action:
                    if 'main' in action:
                        self._screenlist = deque(
                            [self._ms, self._ts, self._zs, self._ns1, self._ns2, self._gs, self._ss])
                    elif 'left' in action:
                        self._screenlist.rotate(1)
                    elif 'right' in action:
                        self._screenlist.rotate(-1)
                    self.CurrentScreenObject = self._screenlist[0]
                    self.CurrentScreenObject.init()
                    self.CurrentScreenObject.draw()

                if 'rising_sec' in keys:
                    return 'time'
                return True

        return False

    def btn_naming(self, keys, event, button):
        if button & 0x0001:
            keys.append(event + '_left')
        if button & 0x0002:
            keys.append(event + '_up')
        if button & 0x0004:
            keys.append(event + '_ok')
        if button & 0x0008:
            keys.append(event + '_down')
        if button & 0x0010:
            keys.append(event + '_right')
        return keys

    def get_screen_label(self):
        return self.CurrentScreenObject.label

    def get_unsaved_params(self):
        if self.CurrentScreenObject.unsaved_params:
            self.CurrentScreenObject.unsaved_params = False
            return self.CurrentScreenObject.GetEditorParams()
        return None

    def refresh_data(self, label, *args):
        for screen in self._screenlist:
            if label == screen.label:
                screen.refresh_data(*args)
