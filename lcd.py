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
        StdScreen.__init__(self, display)
        self._label = label
        self._settings = settings

    def refresh_data(self):

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

    def EnterListMode(self):
        self.refresh_data()
        tm = time.localtime()

        strings = [
            time.strftime("%T", tm),
            time.strftime("%d.%m.%y", tm),
            'Спутн:{:d}'.format(self._sats),
            'Время:{:s}'.format(self._time_src),
            'Синхр:{:s}'.format(self._pps_src)]

        StdScreen.EnterListMode(self, strings)

    def EnterEditMode(self):
        return

    def ExitEditMode(self):
        return

    def Draw(self):
        # print('Main Draw')

        self.GLCD.Clear()

        self.GLCD.SetFont(Terminus18m)
        self.GLCD.DrawString(0, 0, self.ListModeLines[0])
        self.GLCD.DrawString(0, 15, self.ListModeLines[1])

        self.GLCD.SetFont(Terminus12m)
        self.GLCD.DrawString(64, 0, self.ListModeLines[2])
        self.GLCD.DrawString(64, 11, self.ListModeLines[3])
        self.GLCD.DrawString(64, 22, self.ListModeLines[4])