from abc import ABC, abstractmethod


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

