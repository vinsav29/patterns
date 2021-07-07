# from __future__ import annotations
from abc import ABC, abstractmethod
import time

from .glcdlib import *
from .font.font_terminus12m import *
from .font.font_terminus18m import *

# ------------------------------------------------------------------------------

# MODE_LIST = 0
# MODE_EDIT = 1
# MODE_MSSG = 2

CP_LEFT = chr(0x040a)
CP_UP = chr(0x040c)
CP_RIGHT = chr(0x040b)
CP_DOWN = chr(0x040f)
CP_OK = chr(0x040e)

CP_YES = chr(0x0402)
CP_NO = chr(0x0403)


class Mode(ABC):
    """
    Базовый класс Состояния объявляет методы, которые должны реализовать все
    Конкретные Состояния, а также предоставляет обратную ссылку на объект
    Контекст, связанный с Состоянием. Эта обратная ссылка может использоваться
    Состояниями для передачи Контекста другому Состоянию.
    """

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, screen) -> None:
        self._screen = screen

    # @abstractmethod
    # def action(self, keys) -> None:
    #     pass

    def reset_screenlist(self):
        # print('Abstract method reset_screenlist')
        return 'rotate_main'

    def press_left(self):
        # print('Abstract method press left')
        return 'rotate_left'

    def press_right(self):
        # print('Abstract method press_right')
        return 'rotate_right'

    def press_down(self):
        pass

    def press_up(self):
        pass

    def press_ok(self):
        pass

    def event_sec(self):
        pass

    def draw(self):
        pass


class ListMode(Mode):
    def __init__(self):
        # print('List mode constructor')
        # self.screen.refresh_data()
        #
        # self.screen.window_pos = 0
        # self.screen.list_pos = 0
        # self.screen.list_end = len(self.screen.strings) - 1
        pass

    def press_down(self):
        # print('press_down in Listmode')
        if self.screen.list_pos < self.screen.list_end:
            self.screen.list_pos += 1
            if self.screen.list_pos > (self.screen.window_pos + 1):
                self.screen.window_pos += 1
        self.screen.draw()
        return 'no action'

    def press_up(self):
        # print('press_up in Listmode')
        if self.screen.list_pos > 0:
            self.screen.list_pos -= 1
            if self.screen.list_pos < self.screen.window_pos:
                self.screen.window_pos -= 1
        self.screen.draw()
        return 'no action'

    def press_ok(self):
        # print('rising_ok in Listmode')
        self.screen.EnterEditMode()     # empty for MainScreen
        self.screen.draw()
        return 'no action'

    def event_sec(self):
        self.screen.refresh_data()
        self.screen.draw()
        return 'no action'

    def draw(self):
        # print('draw in Listmode')

        # print(self.screen.list_pos, self.screen.list_end, self.screen.window_pos)
        # print(self.screen.strings)
        cursor = ['  ', '  ']

        self.screen.GLCD.Clear()
        self.screen.GLCD.SetFont(Terminus12m)

        self.screen.GLCD.DrawChar(0, 0, CP_LEFT)
        self.screen.GLCD.DrawChar(115, 0, CP_RIGHT)

        label_pos = (122 - len(self.screen.label) * 6) // 2
        self.screen.GLCD.DrawString(label_pos, 0, self.screen.label)
        self.screen.GLCD.DrawLine(0, 10, 121, 10, 1)

        scroll_y = 22 if self.screen.window_pos < self.screen.list_pos else 11
        self.screen.GLCD.DrawChar(0, scroll_y, CP_RIGHT)
        # TODO: remove this
        if scroll_y == 22:
            cursor[1] = '> '
        else:
            cursor[0] = '> '

        if self.screen.window_pos > 0:
            self.screen.GLCD.DrawChar(115, 11, CP_UP)
        if self.screen.window_pos < (self.screen.list_end - 1):
            self.screen.GLCD.DrawChar(115, 22, CP_DOWN)

        for n in range(2):
            y = n * 11 + 11
            w = self.screen.window_pos + n
            if w < len(self.screen.strings):
                string = self.screen.strings[w]
                self.screen.GLCD.DrawString(6, y, string)

                # print(cursor[n], string)


class EditMode(Mode):
    def __init__(self):
    #     if len(self.screen.strings) == 0:
    #         return
    #
    #     self.screen.list_end = len(self.screen.EditModeLines) - 1
    #
    #     index = 0
    #     for symbol in self.screen.EditModeMap:
    #         if symbol[0] == self.screen.list_pos:
    #             self.screen.editor_pos = index
    #             break
    #         index += 1
        pass

    def press_left(self):
        # print('press_left in EditMode')
        if self.screen.editor_pos > 0:
            self.screen.editor_pos -= 1
            self.screen.list_pos = self.screen.EditModeMap[self.screen.editor_pos][0]
            if self.screen.list_pos < self.screen.window_pos:
                self.screen.window_pos -= 1
        self.screen.draw()
        return 'no action'

    def press_right(self):
        # print('press_right in EditMode')
        end = len(self.screen.EditModeMap) - 1
        if self.screen.editor_pos < end:
            self.screen.editor_pos += 1
            self.screen.list_pos = self.screen.EditModeMap[self.screen.editor_pos][0]
            if self.screen.list_pos > (self.screen.window_pos + 1):
                self.screen.window_pos += 1
        self.screen.draw()
        return 'no action'

    def press_down(self):
        # print('press_down in EditMode')

        y, x, type = self.screen.EditModeMap[self.screen.editor_pos]
        char = self.screen.strings[y][x]

        if type == 'd':
            if char == '+':
                char = '-'
            elif char == '-':
                char = '+'
            else:
                char = '9' if char == '0' else chr(ord(char) - 1)

        if type == 'b':
            if char == CP_YES:
                char = CP_NO
            else:
                char = CP_YES

        str = self.screen.strings[y]
        self.screen.strings[y] = str[:x] + char + str[x + 1:]

        self.screen.draw()
        return 'no action'

    def press_up(self):
        # print('press_up in EditMode')

        y, x, type = self.screen.EditModeMap[self.screen.editor_pos]
        char = self.screen.strings[y][x]

        if type == 'd':
            if char == '+':
                char = '-'
            elif char == '-':
                char = '+'
            else:
                char = '0' if char == '9' else chr(ord(char) + 1)

        if type == 'b':
            if char == CP_YES:
                char = CP_NO
            else:
                char = CP_YES

        str = self.screen.strings[y]
        self.screen.strings[y] = str[:x] + char + str[x + 1:]

        self.screen.draw()
        return 'no action'

    def press_ok(self):
        # print('rising_ok in EditMode')
        no_errors = self.screen.ExitEditMode()
        # no_errors = self.screen.verify_data()
        if no_errors:
            self.screen.unsaved_params = True
            self.screen.EnterListMode()
        else:
            self.screen.EnterMessageMode()
        self.screen.draw()
        return 'no action'

    def draw(self):
        # print('draw in EditMode')

        # print(self.screen.list_pos, self.screen.list_end, self.screen.window_pos)
        # print(self.screen.strings)

        self.screen.GLCD.Clear()
        self.screen.GLCD.SetFont(Terminus12m)

        label_pos = (122 - len(self.screen.label) * 6) // 2
        self.screen.GLCD.DrawString(label_pos, 0, self.screen.label)
        self.screen.GLCD.DrawLine(0, 10, 121, 10, 1)

        scroll_y = 22 if self.screen.window_pos < self.screen.list_pos else 11
        self.screen.GLCD.DrawChar(0, scroll_y, CP_RIGHT)

        if self.screen.window_pos > 0:
            self.screen.GLCD.DrawChar(115, 11, CP_UP)
        if self.screen.window_pos < (self.screen.list_end - 1):
            self.screen.GLCD.DrawChar(115, 22, CP_DOWN)

        for n in range(2):
            y = n * 11 + 11
            w = self.screen.window_pos + n
            if w < len(self.screen.strings):
                cursor = -1
                if (self.screen.list_pos - self.screen.window_pos) == n:
                    cursor = self.screen.EditModeMap[self.screen.editor_pos][1]
                string = self.screen.strings[w]
                self.screen.GLCD.DrawStringSelect(6, y, string, cursor, cursor)

                # print(cursor, string)


class MessageMode(Mode):
    def __init__(self):
        # self.screen.msg_pos = 0
        # self.screen.MessageLines = message
        # self.screen.msg_end = len(message) - 1
        pass

    def press_down(self):
        # print('press_down in MessageMode')
        if self.screen.msg_pos < (self.screen.msg_end - 1):
            self.screen.msg_pos += 1
        self.screen.draw()
        return 'no action'

    def press_up(self):
        # print('press_up in MessageMode')
        if self.screen.msg_pos > 0:
            self.screen.msg_pos -= 1
        self.screen.draw()
        return 'no action'

    def press_left(self):
        # print('press_left in MessageMode')
        self.screen.EnterListMode()
        self.screen.draw()
        return 'no action'

    def press_ok(self):
        # print('rising_ok in MessageMode')
        self.screen.EnterEditMode()
        self.screen.draw()
        return 'no action'

    def draw(self):
        # print('draw in MessageMode')

        # print(self.screen.list_pos, self.screen.list_end, self.screen.window_pos)
        # print(self.screen.strings)

        self.screen.GLCD.Clear()
        self.screen.GLCD.SetFont(Terminus12m)

        self.screen.GLCD.DrawLine(0, 10, 121, 10, 1)
        self.screen.GLCD.DrawLine(61, 0, 61, 10, 1)
        self.screen.GLCD.DrawString(5, 0, CP_OK + ' OK')
        self.screen.GLCD.DrawString(66, 0, CP_LEFT + ' Отмена')

        for n in range(2):
            y = n * 11 + 11
            w = self.screen.msg_pos + n
            if w < len(self.screen.MessageLines):
                string = self.screen.MessageLines[w]
                self.screen.GLCD.DrawString(6, y, string)
                # print(string)

        if self.screen.msg_pos > 0:
            self.screen.GLCD.DrawChar(115, 11, CP_UP)
        if self.screen.msg_pos < (self.screen.msg_end - 1):
            self.screen.GLCD.DrawChar(115, 22, CP_DOWN)


class StdScreen:
    def __init__(self, display):
        self.label = ''
        self._mode = None
        self.unsaved_params = False

        self.strings = []
        self.list_end = 0
        self.list_pos = 0
        self.window_pos = 0

        self.editor_pos = 0

        self.message = []
        self.msg_pos = 0
        self.msg_end = 0

        self.GLCD = display
        # self.Mode = MODE_LIST
        # self.LastMode = MODE_LIST
        # self.WindowPos = 0
        # self.ListPos = 0
        # self.ListEnd = 0
        # self.EditorPos = 0
        # self.MsgPos = 0
        # self.MsgEnd = 0
        self.ListModeLines = []
        self.EditModeLines = []
        self.EditModeMap = []
        self.EditModeParams = []

        self.MessageLines = []

    def init(self):
        # self.transition_to(ListMode())
        # self.refresh_data()
        #
        # self.window_pos = 0
        # self.list_pos = 0
        # self.list_end = len(self.strings) - 1
        self.EnterListMode()

        return self

    def refresh_data(self):
        pass

    def EnterListMode(self):
        self.transition_to(ListMode())
        self.refresh_data()

        self.window_pos = 0
        self.list_pos = 0
        self.list_end = len(self.strings) - 1

    def EnterEditMode(self):
        # print('StdScreen EnterEditMode')
        self.transition_to(EditMode())

        if len(self.strings) == 0:
            return

        self.list_end = len(self.EditModeLines) - 1

        index = 0
        for symbol in self.EditModeMap:
            if symbol[0] == self.list_pos:
                self.editor_pos = index
                break
            index += 1

    def ExitEditMode(self):
        pass

    def EnterMessageMode(self):
        # print('StdScreen EnterMessageMode')
        self.transition_to(MessageMode())

        self.msg_pos = 0
        self.MessageLines = self.message
        self.msg_end = len(self.message) - 1

    def CreateEditorMap(self, strings):
        self.EditModeMap = []
        self.EditModeLines = []
        self.EditModeParams = []
        y_index = 0

        for line in strings:
            begin = 0
            end = 0
            type = ''
            x_index = 0
            open = False
            out = ''
            param = 0
            line_params = []

            for char in line:
                if char == '[':
                    begin = x_index
                    if open == False:
                        open = True
                        type = ''
                        continue
                    else:
                        open = False

                if char in ['d', 'x', 'c', 'b']:  # эти символы возможны в данных!!!
                    if open == True:
                        type = char
                        continue

                if char == ']':  # эти символы возможны в данных!!!
                    end = x_index
                    if open:
                        open = False
                        param += 1
                        for x in range(begin, end):
                            self.EditModeMap.append((y_index, x, type))
                        line_params.append((begin, end))
                        continue

                out += char
                x_index += 1

            self.EditModeParams.append(line_params)
            self.EditModeLines.append(out)
            y_index += 1
        # print(self.EditModeMap, self.EditModeLines, self.EditModeParams)

    def GetEditorParams(self):
        params_list = []
        y_index = 0
        for line in self.EditModeParams:
            params_line = []
            for pos in line:
                begin, end = pos
                string = self.strings[y_index][begin:end]
                params_line.append(string)
            params_list.append(params_line)
            y_index += 1
        return params_list

    def transition_to(self, mode: Mode):
        """
        Контекст позволяет изменять объект Состояния во время выполнения.
        """

        # print(type(self).__name__, type(mode).__name__)
        self._mode = mode
        self._mode.screen = self

    def action(self, keys):
        if 'clamping_left' in keys:
            # print('clamping_left')
            return self._mode.reset_screenlist()

        if 'rising_left' in keys:
            # print('rising_left')
            return self._mode.press_left()

        if 'rising_right' in keys:
            # print('rising_right')
            return self._mode.press_right()

        if 'rising_down' in keys:
            # print('rising_down')
            return self._mode.press_down()

        if 'rising_up' in keys:
            # print('rising_up')
            return self._mode.press_up()

        if 'rising_ok' in keys:
            # print('rising_ok')
            return self._mode.press_ok()

        if 'rising_sec' in keys:
            return self._mode.event_sec()

        if keys is not None:
            self.draw()

        return 'no_action'

    def draw(self):
        return self._mode.draw()
