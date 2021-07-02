from __future__ import annotations
from abc import ABC, abstractmethod


class Context:
    """
    Контекст определяет интерфейс, представляющий интерес для клиентов. Он также
    хранит ссылку на экземпляр подкласса Состояния, который отображает текущее
    состояние Контекста.
    """

    _state = None
    """
    Ссылка на текущее состояние Контекста.
    """

    def __init__(self, state: State) -> None:
        self.transition_to(state)

    def transition_to(self, state: State):
        """
        Контекст позволяет изменять объект Состояния во время выполнения.
        """

        print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    """
    Контекст делегирует часть своего поведения текущему объекту Состояния.
    """

    def action(self, button):
        self._state.action(button)

    def request2(self):
        self._state.handle2()


class State(ABC):
    """
    Базовый класс Состояния объявляет методы, которые должны реализовать все
    Конкретные Состояния, а также предоставляет обратную ссылку на объект
    Контекст, связанный с Состоянием. Эта обратная ссылка может использоваться
    Состояниями для передачи Контекста другому Состоянию.
    """

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def action(self, button) -> None:
        pass

    @abstractmethod
    def handle2(self) -> None:
        pass


"""
Конкретные Состояния реализуют различные модели поведения, связанные с
состоянием Контекста.
"""


class ListMode(State):
    def action(self, button) -> None:
        print("ListMode handles request1.")
        if button == 'ok':
            print("ListMode wants to change the state of the context.")
            self.context.transition_to(EditMode())

    def handle2(self) -> None:
        print("ListMode handles request2.")


class EditMode(State):
    def __init__(self):
        print("EditMode activate")

    def action(self, button) -> None:
        print("EditMode handles OK.")
        if button == 'ok':
            print("EditMode wants to change the state of the context.")
            self.context.transition_to(ListMode())

    def handle2(self) -> None:
        print("EditMode handles request2.")
        print("EditMode wants to change the state of the context.")
        self.context.transition_to(ListMode())


if __name__ == "__main__":
    # Клиентский код.

    context = Context(ListMode())
    context.action('ok')
    print()
    # context.request2()
    context.action('ok')