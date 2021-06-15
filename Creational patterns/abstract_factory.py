from __future__ import annotations
from abc import ABC, abstractmethod


class FurnitureFactory(ABC):
    """
    Интерфейс Абстрактной Фабрики объявляет набор методов, которые возвращают
    различные абстрактные продукты. Эти продукты называются семейством и связаны
    темой или концепцией высокого уровня. Продукты одного семейства обычно могут
    взаимодействовать между собой. Семейство продуктов может иметь несколько
    вариаций, но продукты одной вариации несовместимы с продуктами другой.
    """
    @abstractmethod
    def create_chair(self) -> Chair:
        pass

    @abstractmethod
    def create_table(self) -> Table:
        pass


class VictorianFurnitureFactory(FurnitureFactory):
    """
    Конкретная Фабрика производит семейство продуктов одной вариации. Фабрика
    гарантирует совместимость полученных продуктов. Обратите внимание, что
    сигнатуры методов Конкретной Фабрики возвращают абстрактный продукт, в то
    время как внутри метода создается экземпляр конкретного продукта.
    """

    def create_chair(self) -> Chair:
        return VictorianChair()

    def create_table(self) -> Table:
        return VictorianTable()


class ModernFurnitureFactory(FurnitureFactory):
    """
    Каждая Конкретная Фабрика имеет соответствующую вариацию продукта.
    """

    def create_chair(self) -> Chair:
        return ModernChair()

    def create_table(self) -> Table:
        return ModernTable()


class Chair(ABC):
    """
    Каждый отдельный продукт семейства продуктов должен иметь базовый интерфейс.
    Все вариации продукта должны реализовывать этот интерфейс.
    """

    @abstractmethod
    def sit_on_chair(self) -> str:
        pass


"""
Конкретные продукты создаются соответствующими Конкретными Фабриками.
"""


class VictorianChair(Chair):
    def sit_on_chair(self) -> str:
        return "Sit on VictorianChair"


class ModernChair(Chair):
    def sit_on_chair(self) -> str:
        return "Sit on ModernChair"


class Table(ABC):
    """
    Базовый интерфейс другого продукта. Все продукты могут взаимодействовать
    друг с другом, но правильное взаимодействие возможно только между продуктами
    одной и той же конкретной вариации.
    """
    @abstractmethod
    def use_table(self) -> None:
        """
        Продукт B способен работать самостоятельно...
        """
        pass

    @abstractmethod
    def use_table_with_chair(self, collaborator: Chair) -> None:
        """
        ...а также взаимодействовать с Продуктами A той же вариации.

        Абстрактная Фабрика гарантирует, что все продукты, которые она создает,
        имеют одинаковую вариацию и, следовательно, совместимы.
        """
        pass


"""
Конкретные Продукты создаются соответствующими Конкретными Фабриками.
"""


class VictorianTable(Table):
    def use_table(self) -> str:
        return "Use VictorianTable"

    """
    Продукт B1 может корректно работать только с Продуктом A1. Тем не менее, он
    принимает любой экземпляр Абстрактного Продукта А в качестве аргумента.
    """

    def use_table_with_chair(self, collaborator: Chair) -> str:
        result = collaborator.sit_on_chair()
        return f"The result of the VictorianTable collaborating with the ({result})"


class ModernTable(Table):
    def use_table(self) -> str:
        return "Use ModernTable"

    def use_table_with_chair(self, collaborator: Chair):
        """
        Продукт B2 может корректно работать только с Продуктом A2. Тем не менее,
        он принимает любой экземпляр Абстрактного Продукта А в качестве
        аргумента.
        """
        result = collaborator.sit_on_chair()
        return f"The result of the ModernTable collaborating with the ({result})"


def client_code(factory: FurnitureFactory) -> None:
    """
    Клиентский код работает с фабриками и продуктами только через абстрактные
    типы: Абстрактная Фабрика и Абстрактный Продукт. Это позволяет передавать
    любой подкласс фабрики или продукта клиентскому коду, не нарушая его.
    """
    chair = factory.create_chair()
    table = factory.create_table()

    print(f"{table.use_table()}")
    print(f"{table.use_table_with_chair(chair)}", end="")


if __name__ == "__main__":
    """
    Клиентский код может работать с любым конкретным классом фабрики.
    """
    print("Client: Testing client code with the first factory type:")
    client_code(VictorianFurnitureFactory())

    print("\n")

    print("Client: Testing the same client code with the second factory type:")
    client_code(ModernFurnitureFactory())