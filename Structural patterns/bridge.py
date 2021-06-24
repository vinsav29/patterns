from __future__ import annotations
from abc import ABC, abstractmethod


class Shape:
    """
    Абстракция устанавливает интерфейс для «управляющей» части двух иерархий
    классов. Она содержит ссылку на объект из иерархии Реализации и делегирует
    ему всю настоящую работу.
    """

    def __init__(self, color: Color) -> None:
        self.color = color

    def shape_operation(self) -> str:
        return (f"Abstract shape: Base operation with:\n"
                f"{self.color.color_operation()}")


class Circle(Shape):
    """
    Можно расширить Абстракцию без изменения классов Реализации.
    """

    def shape_operation(self) -> str:
        return (f"Circle shape: Circle operation:\n"
                f"{self.color.color_operation()}")


class Color(ABC):
    """
    Реализация устанавливает интерфейс для всех классов реализации. Он не должен
    соответствовать интерфейсу Абстракции. На практике оба интерфейса могут быть
    совершенно разными. Как правило, интерфейс Реализации предоставляет только
    примитивные операции, в то время как Абстракция определяет операции более
    высокого уровня, основанные на этих примитивах.
    """

    @abstractmethod
    def color_operation(self) -> str:
        pass


"""
Каждая Конкретная Реализация соответствует определённой платформе и реализует
интерфейс Реализации с использованием API этой платформы.
"""


class Red(Color):
    def color_operation(self) -> str:
        return "Red color: Here's the result with red."


class Blue(Color):
    def color_operation(self) -> str:
        return "Blue color: Here's the result with blue."


def client_code(shape: Shape) -> None:
    """
    За исключением этапа инициализации, когда объект Абстракции связывается с
    определённым объектом Реализации, клиентский код должен зависеть только от
    класса Абстракции. Таким образом, клиентский код может поддерживать любую
    комбинацию абстракции и реализации.
    """

    # ...

    print(shape.shape_operation(), end="")

    # ...


if __name__ == "__main__":
    """
    Клиентский код должен работать с любой предварительно сконфигурированной
    комбинацией абстракции и реализации.
    """

    color = Red()
    shape = Shape(color)
    client_code(shape)

    print("\n")

    color = Blue()
    shape = Circle(color)
    client_code(shape)