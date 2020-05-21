from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points,
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(ABC, Hero):
    def __init__(self, base):
        self.base = base
        self.basic_feature = ("Strength", "Endurance", "Agility", "Luck", "Perception", "Charisma", "Intelligence")

    @abstractmethod
    def get_positive_effects(self):
        return self.positive_effects

    @abstractmethod
    def get_negative_effects(self):
        return self.negative_effects

    @abstractmethod
    def get_stats(self):
        pass

class AbstractPositive(AbstractEffect):
    def get_negative_effects(self):
        return self.base.get_negative_effects()


class AbstractNegative(AbstractEffect):
    def get_positive_effects(self):
        return self.base.get_positive_effects()


class Berserk(AbstractPositive):
    # Увеличивает характеристики: Сила, Выносливость, Ловкость, Удача на 7;
    # уменьшает характеристики: Восприятие, Харизма, Интеллект на 3;
    # количество единиц здоровья увеличивается на 50.
    def get_positive_effects(self):
        return self.base.get_positive_effects() + ["Berserk"]

    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] += 7
        stats["Endurance"] += 7
        stats["Agility"] += 7
        stats["Luck"] += 7
        stats["Perception"] -= 3
        stats["Charisma"] -= 3
        stats["Intelligence"] -= 3
        stats["HP"] += 50
        return stats


class Blessing(AbstractPositive):
    # Увеличивает все основные характеристики на 2.
    def get_positive_effects(self):
        return self.base.get_positive_effects() + ["Blessing"]

    def get_stats(self):
        stats = self.base.get_stats()
        for i in self.basic_feature:
            stats[i] += 2
        return stats

class Weakness(AbstractNegative):
    # Уменьшает характеристики: Сила, Выносливость, Ловкость на 4.
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['Weakness']

    def get_stats(self):
        stats = self.base.get_stats()
        stats["Strength"] -= 4
        stats["Endurance"] -= 4
        stats["Agility"] -= 4
        return stats


class Curse(AbstractNegative):
    # Уменьшает  характеристику Удача на 10.
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['Curse']

    def get_stats(self):
        stats = self.base.get_stats()
        for i in self.basic_feature:
            stats[i] -= 2
        return stats


class EvilEye(AbstractNegative):
    # Уменьшает все основные характеристики на 2.
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['EvilEye']

    def get_stats(self):
        stats = self.base.get_stats()
        stats["Luck"] -= 10
        return stats


hero = Hero()
print(hero.get_stats())
print(hero.stats)
print(hero.get_negative_effects())
print(hero.get_positive_effects())

# # накладываем эффект
brs1 = Berserk(hero)
print(brs1.get_stats())
print(brs1.get_negative_effects())
print(brs1.get_positive_effects())
#
# # накладываем эффекты
brs2 = Berserk(brs1)
cur1 = Curse(brs2)
print(cur1.get_stats())
print(cur1.get_positive_effects())
print(cur1.get_negative_effects())
#
# # снимаем эффект Berserk
cur1.base = brs1
print(cur1.get_stats())
print(cur1.get_positive_effects())
print(cur1.get_negative_effects())

