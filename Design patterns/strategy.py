from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class StdScreen:
    """
    Контекст определяет интерфейс, представляющий интерес для клиентов.
    """

    def __init__(self, mode: Mode) -> None:
        """
        Обычно Контекст принимает стратегию через конструктор, а также
        предоставляет сеттер для её изменения во время выполнения.
        """

        self._mode = mode
        self._label = 'Label'

    @property
    def mode(self) -> Mode:
        """
        Контекст хранит ссылку на один из объектов Стратегии. Контекст не знает
        конкретного класса стратегии. Он должен работать со всеми стратегиями
        через интерфейс Стратегии.
        """

        return self._mode

    @mode.setter
    def mode(self, mode: Mode) -> None:
        """
        Обычно Контекст позволяет заменить объект Стратегии во время выполнения.
        """

        self._mode = mode

    def do_some_business_logic(self) -> None:
        """
        Вместо того, чтобы самостоятельно реализовывать множественные версии
        алгоритма, Контекст делегирует некоторую работу объекту Стратегии.
        """

        # ...
        print(self._label)
        print("StdScreen: Sorting data using the strategy (not sure how it'll do it)")
        result = self._mode.do_algorithm(["a", "b", "c", "d", "e"])
        print(",".join(result))

        # ...


class Mode(ABC):
    """
    Интерфейс Стратегии объявляет операции, общие для всех поддерживаемых версий
    некоторого алгоритма.

    Контекст использует этот интерфейс для вызова алгоритма, определённого
    Конкретными Стратегиями.
    """

    @abstractmethod
    def do_algorithm(self, data: List):
        pass


"""
Конкретные Стратегии реализуют алгоритм, следуя базовому интерфейсу Стратегии.
Этот интерфейс делает их взаимозаменяемыми в Контексте.
"""


class ListMode(Mode):
    def do_algorithm(self, data: List) -> List:
        return sorted(data)


class EditMode(Mode):
    def __init__(self):
        print("EditMode activated")

    def do_algorithm(self, data: List) -> List:
        return reversed(sorted(data))


if __name__ == "__main__":
    # Клиентский код выбирает конкретную стратегию и передаёт её в контекст.
    # Клиент должен знать о различиях между стратегиями, чтобы сделать
    # правильный выбор.

    screen = StdScreen(ListMode())
    print("Client: mode is set to list mode.")
    screen.do_some_business_logic()
    print()

    print("Client: mode is set to edit mode.")
    screen.mode = EditMode()
    screen.do_some_business_logic()