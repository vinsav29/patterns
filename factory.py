from __future__ import annotations
from abc import ABC, abstractmethod


class Logistics(ABC):
    """
    Класс Создатель объявляет фабричный метод, который должен возвращать объект
    класса Продукт. Подклассы Создателя обычно предоставляют реализацию этого
    метода.
    """

    @abstractmethod
    def create_transport(self):
        """
        Обратите внимание, что Создатель может также обеспечить реализацию
        фабричного метода по умолчанию.
        """
        pass

    def plan_delivery(self) -> Transport:
        """
        Также заметьте, что, несмотря на название, основная обязанность
        Создателя не заключается в создании продуктов. Обычно он содержит
        некоторую базовую бизнес-логику, которая основана на объектах Продуктов,
        возвращаемых фабричным методом. Подклассы могут косвенно изменять эту
        бизнес-логику, переопределяя фабричный метод и возвращая из него другой
        тип продукта.
        """

        # Вызываем фабричный метод, чтобы получить объект-продукт.
        transport = self.create_transport()

        # Далее, работаем с этим продуктом.
        print(f"Creator: The same creator's code has just worked with {transport.deliver()}")

        return transport


"""
Конкретные Создатели переопределяют фабричный метод для того, чтобы изменить тип
результирующего продукта.
"""


class RoadLogistics(Logistics):
    """
    Обратите внимание, что сигнатура метода по-прежнему использует тип
    абстрактного продукта, хотя фактически из метода возвращается конкретный
    продукт. Таким образом, Создатель может оставаться независимым от конкретных
    классов продуктов.
    """

    def create_transport(self) -> Transport:
        return Truck()


class SeaLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Ship()


class Transport(ABC):
    """
    Интерфейс Продукта объявляет операции, которые должны выполнять все
    конкретные продукты.
    """

    @abstractmethod
    def deliver(self) -> str:
        pass


"""
Конкретные Продукты предоставляют различные реализации интерфейса Продукта.
"""


class Truck(Transport):
    def deliver(self) -> str:
        return "{Truck delivery}"


class Ship(Transport):
    def deliver(self) -> str:
        return "{Ship delivery}"


def client_code(logistics: Logistics) -> Transport:
    """
    Клиентский код работает с экземпляром конкретного создателя, хотя и через
    его базовый интерфейс. Пока клиент продолжает работать с создателем через
    базовый интерфейс, вы можете передать ему любой подкласс создателя.
    """

    print(f"Client: I'm not aware of the logistic class, just plan delivery.")
    return logistics.plan_delivery()


if __name__ == "__main__":
    print("App: Launched with the RoadLogistics.")
    truck = client_code(RoadLogistics())

    print("App: Launched with the SeaLogistics.")
    ship = client_code(SeaLogistics())

    print(truck.deliver())
    print(ship.deliver())