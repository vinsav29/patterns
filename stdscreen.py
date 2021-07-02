# from .glcdlib import *
# from .font.font_terminus12m import *
# from .font.font_terminus18m import *
from __future__ import annotations
from abc import ABC, abstractmethod
import time

# ------------------------------------------------------------------------------

MODE_LIST = 0
MODE_EDIT = 1
MODE_MSSG = 2

CP_LEFT = chr(0x040a)
CP_UP = chr(0x040c)
CP_RIGHT = chr(0x040b)
CP_DOWN = chr(0x040f)
CP_OK = chr(0x040e)

CP_YES = chr(0x0402)
CP_NO = chr(0x0403)


class StdScreen:
    def __init__(self, display, mode: Mode):
        self._mode = None
        self.strings = []
        self.list_end = 0
        self.list_pos = 0
        self.window_pos = 0
        self.init()
        self.transition_to(mode)

        self.GLCD = display
        self.Mode = MODE_LIST
        self.LastMode = MODE_LIST
        self.WindowPos = 0
        self.ListPos = 0
        self.ListEnd = 0
        self.EditorPos = 0
        self.MsgPos = 0
        self.MsgEnd = 0
        self.ListModeLines = []
        self.EditModeLines = []
        self.EditModeMap = []
        self.EditModeParams = []
        self._label = ''
        self.MessageLines = []
        self.unsaved_params = False

    def init(self):
        self.refresh_data()
        self.window_pos = 0
        self.list_pos = 0
        self.list_end = len(self.strings) - 1
        # self.EnterListMode()
        return self

    def refresh_data(self):
        tm = time.localtime()
        self.strings = [
            time.strftime("Время: %T", tm),
            time.strftime("Дата: %d.%m.%y", tm),
        ]

    def EnterListMode(self, Strings):
        self.Mode = MODE_LIST
        self.ListModeLines = Strings
        self.ListEnd = len(Strings) - 1

    def ExitListMode(self):
        self.EditModeMap = []
        self.EditModeLines = []
        self.EditModeParams = []

    def EnterEditMode(self, Strings):
        if len(Strings) == 0:
            return

        self.CreateEditorMap(Strings)
        self.ListEnd = len(self.EditModeLines) - 1

        index = 0
        for symbol in self.EditModeMap:
            if symbol[0] == self.ListPos:
                self.EditorPos = index
                self.Mode = MODE_EDIT
                break
            index += 1

    def ExitEditMode(self):
        self.Mode = MODE_LIST
        self.EditModeMap = []

    def EnterMessageMode(self, Strings):
        self.MsgPos = 0
        self.LastMode = self.Mode
        self.Mode = MODE_MSSG
        self.MessageLines = Strings
        self.MsgEnd = len(Strings) - 1

    def ExitMessageMode(self):
        self.Mode = self.LastMode
        self.MessageLines = []

    def CreateEditorMap(self, Strings):
        self.EditModeMap = []
        self.EditModeLines = []
        self.EditModeParams = []
        y_index = 0

        for line in Strings:
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
                    if open == True:
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

    def GetEditorParams(self):
        params_list = []
        y_index = 0
        for line in self.EditModeParams:
            params_line = []
            for pos in line:
                begin, end = pos
                string = self.EditModeLines[y_index][begin:end]
                params_line.append(string)
            params_list.append(params_line)
            y_index += 1
        return params_list

    def Actions(self, Keys):
        if 'clamping_left' in Keys:
            self.ExitListMode()
            return 'rotate_main'

        if self.Mode == MODE_LIST:
            if 'rising_left' in Keys:
                self.ExitListMode()
                return 'rotate_left'

            if 'rising_right' in Keys:
                self.ExitListMode()
                return 'rotate_right'

            if 'rising_down' in Keys:
                if self.ListPos < self.ListEnd:
                    self.ListPos += 1
                    if self.ListPos > (self.WindowPos + 1):
                        self.WindowPos += 1

            if 'rising_up' in Keys:
                if self.ListPos > 0:
                    self.ListPos -= 1
                    if self.ListPos < self.WindowPos:
                        self.WindowPos -= 1

            if 'rising_ok' in Keys:
                self.ExitListMode()
                self.EnterEditMode()

            if 'rising_sec' in Keys:
                self.EnterListMode()

            if Keys is not None:
                self.Draw()

        elif self.Mode == MODE_EDIT:
            if 'rising_left' in Keys:
                if self.EditorPos > 0:
                    self.EditorPos -= 1
                    self.ListPos = self.EditModeMap[self.EditorPos][0]
                    if self.ListPos < self.WindowPos:
                        self.WindowPos -= 1

            if 'rising_right' in Keys:
                end = len(self.EditModeMap) - 1
                if self.EditorPos < end:
                    self.EditorPos += 1
                    self.ListPos = self.EditModeMap[self.EditorPos][0]
                    if self.ListPos > (self.WindowPos + 1):
                        self.WindowPos += 1

            if 'rising_down' in Keys:
                y, x, type = self.EditModeMap[self.EditorPos]
                char = self.EditModeLines[y][x]

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

                str = self.EditModeLines[y]
                self.EditModeLines[y] = str[:x] + char + str[x + 1:]

            if 'rising_up' in Keys:
                y, x, type = self.EditModeMap[self.EditorPos]
                char = self.EditModeLines[y][x]

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

                str = self.EditModeLines[y]
                self.EditModeLines[y] = str[:x] + char + str[x + 1:]

            if 'rising_ok' in Keys:
                no_errors = self.ExitEditMode()
                if no_errors:
                    self.unsaved_params = True

            if Keys is not None:
                self.Draw()

        elif self.Mode == MODE_MSSG:
            if 'rising_down' in Keys:
                if self.MsgPos < (self.MsgEnd - 1):
                    self.MsgPos += 1

            if 'rising_up' in Keys:
                if self.MsgPos > 0:
                    self.MsgPos -= 1

            if 'rising_ok' in Keys:
                self.ExitMessageMode()

            if 'rising_left' in Keys:
                self.ExitMessageMode()
                self.EnterListMode()

            if Keys is not None:
                self.Draw()

        return 'no_action'
        # return self

    def Draw(self):
        print(self.strings)
        # self.GLCD.Clear()
        # self.GLCD.SetFont(Terminus12m)
        #
        # if self.Mode == MODE_LIST:
        #     self.GLCD.DrawChar(0, 0, CP_LEFT)
        #     self.GLCD.DrawChar(115, 0, CP_RIGHT)
        #
        # if (self.Mode == MODE_LIST) | (self.Mode == MODE_EDIT):
        #     label_pos = (122 - len(self._label) * 6) // 2
        #     self.GLCD.DrawString(label_pos, 0, self._label)
        #     self.GLCD.DrawLine(0, 10, 121, 10, 1)
        #
        #     scroll_y = 22 if self.WindowPos < self.ListPos else 11
        #     self.GLCD.DrawChar(0, scroll_y, CP_RIGHT)
        #
        #     if self.WindowPos > 0:
        #         self.GLCD.DrawChar(115, 11, CP_UP)
        #     if self.WindowPos < (self.ListEnd - 1):
        #         self.GLCD.DrawChar(115, 22, CP_DOWN)
        #
        # if self.Mode == MODE_LIST:
        #     for N in range(2):
        #         Y = N * 11 + 11
        #         W = self.WindowPos + N
        #         if W < len(self.ListModeLines):
        #             string = self.ListModeLines[W]
        #             self.GLCD.DrawString(6, Y, string)
        #
        # if self.Mode == MODE_EDIT:
        #     for N in range(2):
        #         Y = N * 11 + 11
        #         W = self.WindowPos + N
        #         if W < len(self.EditModeLines):
        #             cursor = -1
        #             if (self.ListPos - self.WindowPos) == N:
        #                 cursor = self.EditModeMap[self.EditorPos][1]
        #             string = self.EditModeLines[W]
        #             self.GLCD.DrawStringSelect(6, Y, string, cursor, cursor)
        #
        # if self.Mode == MODE_MSSG:
        #     self.GLCD.DrawLine(0, 10, 121, 10, 1)
        #     self.GLCD.DrawLine(61, 0, 61, 10, 1)
        #     self.GLCD.DrawString(5, 0, CP_OK + ' OK')
        #     self.GLCD.DrawString(66, 0, CP_LEFT + ' Отмена')
        #     for N in range(2):
        #         Y = N * 11 + 11
        #         W = self.MsgPos + N
        #         if W < len(self.MessageLines):
        #             string = self.MessageLines[W]
        #             self.GLCD.DrawString(6, Y, string)
        #
        #     if self.MsgPos > 0:
        #         self.GLCD.DrawChar(115, 11, CP_UP)
        #     if self.MsgPos < (self.MsgEnd - 1):
        #         self.GLCD.DrawChar(115, 22, CP_DOWN)

    def transition_to(self, mode: Mode):
        """
        Контекст позволяет изменять объект Состояния во время выполнения.
        """

        print(f"Context: Transition to {type(mode).__name__}")
        self._mode = mode
        self._mode.context = self
        self.Draw()

    def action(self, keys):
        return self._mode.action(keys)


class Mode(ABC):
    """
    Базовый класс Состояния объявляет методы, которые должны реализовать все
    Конкретные Состояния, а также предоставляет обратную ссылку на объект
    Контекст, связанный с Состоянием. Эта обратная ссылка может использоваться
    Состояниями для передачи Контекста другому Состоянию.
    """

    @property
    def context(self) -> StdScreen:
        return self._context

    @context.setter
    def context(self, context: StdScreen) -> None:
        self._context = context

    @abstractmethod
    def action(self, keys) -> None:
        pass


class ScreenMode(Mode):
    def __init__(self):
        pass

    def action(self, keys):
        if 'clamping_left' in keys:
            self.context.transition_to(ScreenMode())
            return 'rotate_main'

        return 'no_action'


class ListMode(Mode):
    def __init__(self):
        pass

    def action(self, keys):

        if 'clamping_left' in keys:
            self.context.transition_to(ScreenMode())
            return 'rotate_main'

        if 'rising_left' in keys:
            return 'rotate_left'

        if 'rising_right' in keys:
            return 'rotate_right'

        if 'rising_down' in keys:
            if self.list_pos < self.list_end:
                self.list_pos += 1
                if self.list_pos > (self.window_pos + 1):
                    self.window_pos += 1

        if 'rising_up' in keys:
            if self.list_pos > 0:
                self.list_pos -= 1
                if self.list_pos < self.window_pos:
                    self.window_pos -= 1

        if 'rising_ok' in keys:
            print('rising_ok in Listmode')
            self.context.transition_to(EditMode())

        if 'rising_sec' in keys:
            self.context.refresh_data()

        if keys is not None:
            self.context.Draw()

        return 'no_action'


class EditMode(Mode):
    def __init__(self):
        pass

    def action(self, keys):
        print(keys)

        if 'clamping_left' in keys:
            self.context.transition_to(ScreenMode())
            return 'rotate_main'

        if 'rising_left' in keys:
            pass

        if 'rising_right' in keys:
            pass

        if 'rising_down' in keys:
            pass

        if 'rising_up' in keys:
            pass

        if 'rising_ok' in keys:
            print('rising_ok in Editmode')

        if 'rising_sec' in keys:
            pass

        if keys is not None:
            self.context.Draw()

        return 'no_action'


if __name__ == "__main__":
    # Клиентский код.

    lcd = StdScreen(display=None, mode=ListMode())
    # lcd.init()
    for key in ('rising_ok', 'clamping_left', 'rising_sec'):
        time.sleep(0.5)
        print()
        print('Pressed:', key)
        action = lcd.action(key)
        print('action is', action)

        if 'rotate' in action:
            if 'main' in action:
                # self._screenlist = deque([self._ms, self._ts, self._zs, self._ns1, self._ns2, self._gs, self._ss])
                print('set screen to main')
            elif 'left' in action:
                # self._screenlist.rotate(1)
                print('rotate left')
            elif 'right' in action:
                # self._screenlist.rotate(-1)
                print('rotate right')
            lcd = StdScreen(display=None, mode=ListMode())
