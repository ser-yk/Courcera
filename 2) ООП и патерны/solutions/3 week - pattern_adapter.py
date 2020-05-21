# Класс Light создает в методе __init__ поле заданного размера. За размер поля отвечает параметр, представляющий из
# себя кортеж из 2 чисел. Элемент dim[1] отвечает за высоту карты, dim[0] за ее ширину. Метод set_lights
# устанавливает массив источников света с заданными координатами и просчитывает освещение. Метод set_obstacles
# устанавливает препятствия аналогичным образом. Положение элементов задается списком кортежей. В каждом элементе
# кортежа хранятся 2 значения: elem[0] -- координата по ширине карты и elem[1] -- координата по высоте
# соответственно. Метод generate_lights рассчитывает освещенность с учетом источников и препятствий.

class System:
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # Источники света
        self.map[5][2] = -1  # Стены

    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)


class Light:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights):
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        return self.grid.copy()


class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee
        self.lights = list()
        self.obstacles = list()
        self.dim = None

    def lighten(self, grid):
        self.dim = [len(grid), len(grid[0])]
        self.adaptee.set_dim([self.dim[1], self.dim[0]])

        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                if grid[i][j] == 1:
                    self.lights.append((j, i))
                elif grid[i][j] == -1:
                    self.obstacles.append((j, i))

        self.adaptee.set_lights(self.lights)
        self.adaptee.set_obstacles(self.obstacles)

        return self.adaptee.generate_lights()





