from abc import ABC, abstractmethod

class Weapon(ABC):
    def __init__(self, damage):
        self.damage = damage

    @abstractmethod
    def attack(self, enemy):
        pass

    def get_damage(self):
        return self.damage

class Sword(Weapon):
    def __init__(self, damage):
        super().__init__(damage)

    def attack(self, enemy):
        damage = self.get_damage()
        print(f"Завдано {damage} пошкодження мечем")
        enemy.take_damage(damage)

class Gun(Weapon):
    def __init__(self, damage):
        super().__init__(damage)

    def attack(self, enemy):
        damage = self.get_damage()
        print(f"Завдано {damage} пошкодження пістолетом")
        enemy.take_damage(damage)

class Enemy:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def take_damage(self, damage):
        self.health -= damage
        print(f"{self.name} отримав пошкодження {damage}, залишилося здоров'я: {self.health}")
        if self.health <= 0:
            print(f"{self.name} загинув")

    def get_health(self):
        return self.health

    def get_name(self):
        return self.name

# Клас персонажа, який використовує зброю для атаки
class Character:
    def __init__(self, weapon):
        self.weapon = weapon

    def attack(self, enemy):
        print("Атака персонажа")
        self.weapon.attack(enemy)

    def set_weapon(self, weapon):
        self.weapon = weapon

# Приклад використання
if __name__ == "__main__":
    sword = Sword(10)
    gun = Gun(20)

    enemy1 = Enemy("Ворог_1", 100)
    enemy2 = Enemy("Ворог_2", 150)

    character = Character(sword)
    character.attack(enemy1)

    character.set_weapon(gun)
    character.attack(enemy2)
