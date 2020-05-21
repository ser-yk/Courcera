import random
import os
import msvcrt
import copy


import colorama
from colorama import Fore


class Game:
    def __init__(self):
        self.field = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self._check_field = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self._check_motion = set()
        self.score = 0
        self.pressed_key = None
        self.win = None

    def up(self):
        self._count_field()

    def down(self):
        self._revers()
        self._count_field()
        self._revers()

    def right(self):
        self._turn_field('left')
        self._count_field()
        self._turn_field('right')

    def left(self):
        self._turn_field('right')
        self._count_field()
        self._turn_field('left')

    def _revers(self):
        """
        Функция разворачивает матрицу задом наперёд
        """
        rev_field = []
        for row in reversed(self.field):
            new_row = []
            for num in reversed(row):
                new_row.append(num)
            rev_field.append(new_row)
            self.field = rev_field

    def _turn_field(self, direction):
        """
        Функция разворачивает матрицу на 90 градусов влево лио право.
        """
        if direction == 'left':
            turn_field = []
            for column in range(-1, -5, -1):
                new_row = []
                for row in range(4):
                    num = self.field[row][column]
                    new_row.append(num)
                turn_field.append(new_row)
            self.field = turn_field
        elif direction == 'right':
            turn_field = []
            for column in range(4):
                new_row = []
                for row in range(-1, -5, -1):
                    num = self.field[row][column]
                    new_row.append(num)
                turn_field.append(new_row)
            self.field = turn_field

    def _count_field(self):
        """
        Управляющая функция, проводит сложение и смещение чисел на поле
        """
        self._slide()
        self._sum_num()
        self._slide()

    def _slide(self):
        """
        Функция сдвигает все числа на поле к вершнему краю
        """
        for _ in range(3):
            while True:
                old_field = self.field
                for column in range(4):
                    for row in range(3):
                        if self.field[row][column] == 0:
                            self.field[row][column] = self.field[row + 1][column]
                            self.field[row + 1][column] = 0
                if old_field == self.field:
                    break

    def _sum_num(self):
        """
        Функция складает числа на поле
        """
        for row in range(3):
            for column in range(4):
                if self.field[row][column] == self.field[row + 1][column]:
                    self.field[row][column] = self.field[row + 1][column] * 2
                    self.field[row + 1][column] = 0
                    if self.field[row][column] == 2048:
                        self.win = True
                    self.score += self.field[row][column]

    def _check_game(self, key=None):
        """Проверяет на условие, что нет ходов, либо игрок набрал 2048 очков"""
        if self.win:
            return 'Win'
        # Если поле не изменилось, фиксируем все ли стороны попробовали нажать, если все - game over.
        equal = self.check_matrix()
        if equal:
            if key:
                self._check_motion.add(key)
                if len(self._check_motion) == 4:
                    return 'Game Over'
            return
        elif not equal:
            self._check_motion.clear()
            return True

    def check_matrix(self):
        for row in range(4):
            for column in range(4):
                if self._check_field[row][column] == self.field[row][column]:
                    continue
                else:
                    return False
        return True

    def _draw(self):
        pass

    def _save(self):
        pass

    def start_game(self):
        # Рандомно добавляем на поле(в матрицу) число
        self._new_number()
        # Запускаем цикл в котором ждём нажатие клавиш. Реагирует на стрелки. При нажании на ESC завершается цикл.
        while True:
            check = self._check_game(self.pressed_key)
            # Проверяем не окончена ли игра.
            if check is True:
                # Игра продолжается, выкидываем новое число.
                self._new_number()
                self._check_field = copy.deepcopy(self.field)
            elif check == 'Game Over':
                os.system('cls')
                print('Game Over')
                break
            elif check == 'Win':
                os.system('cls')
                print("You're winner!")
                break
            # Вывод на экран
            self._monitor()
            # Жмём клавишу
            self.pressed_key = self._press_key()
            # Случай, когда был нажат Esc
            if self.pressed_key == 'Esc':
                os.system('cls')
                print('Exit')
                break

    def _press_key(self):
        key = msvcrt.getch()
        if ord(key) == 0 or ord(key) == 0xe0:
            key = msvcrt.getch()
            if ord(key) == 72:
                self.up()
                return 'up'
            elif ord(key) == 75:
                self.left()
                return 'left'
            elif ord(key) == 80:
                self.down()
                return 'down'
            elif ord(key) == 77:
                self.right()
                return 'right'
        elif ord(key) == 0x1b:
            return 'Esc'

    def _new_number(self):
        while True:
            self.x = random.randint(0, 3)
            self.y = random.randint(0, 3)
            if self.field[self.x][self.y] == 0:
                self.field[self.x][self.y] = self.value()
                break

    def _monitor(self):
        # Этот метод для вывода обновленной матрицы в консоль, пока нет оболочки
        os.system('cls')
        print(f'Sore:  {self.score: } ')
        print('-' * 16)
        for row in range(4):
            for column in range(4):
                if row == self.x and column == self.y:
                    print(f'{Fore.BLUE}{self.field[row][column]: ^4}{Fore.WHITE}', end='')
                    self.x, self.y = None, None
                else:
                    print(f'{self.field[row][column]: ^4}', end='')
            print('\n')

    @staticmethod
    def value():
        choice_num = [2, 4, 2]
        return random.choice(choice_num)


if __name__ == '__main__':
    colorama.init()
    game = Game()
    game.start_game()
