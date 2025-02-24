import copy


class ElectronicGadget:
    def __init__(self, name):
        self.name = name

    def turn_on(self):
        raise NotImplementedError("Потрібно реалізувати метод 'turn_on' у підкласі.")

    def turn_off(self):
        raise NotImplementedError("Потрібно реалізувати метод 'turn_off' у підкласі.")

    def clone(self):
        return copy.deepcopy(self)


class Phone(ElectronicGadget):
    def turn_on(self):
        print(f"{self.name} телефон увімкнено")

    def turn_off(self):
        print(f"{self.name} телефон вимкнено")


class Laptop(ElectronicGadget):
    def turn_on(self):
        print(f"{self.name} ноутбук увімкнено")

    def turn_off(self):
        print(f"{self.name} ноутбук вимкнено")


if __name__ == "__main__":
    phone1 = Phone("Samsung")
    phone1.turn_on()
    phone1.turn_off()

    laptop1 = Laptop("HP")
    laptop1.turn_on()
    laptop1.turn_off()

    phone2 = phone1.clone()
    phone2.turn_on()
    phone2.turn_off()

    laptop2 = laptop1.clone()
    laptop2.turn_on()
    laptop2.turn_off()

    print("phone1 == phone2:", phone1 == phone2)
    print("laptop1 == laptop2:", laptop1 == laptop2)
