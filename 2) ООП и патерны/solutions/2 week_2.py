import pygame
import random

SCREEN_DIM = (900, 650)


class Vec2d:
    def __init__(self, x_or_pair, y=None):
        if y is None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y

    def __add__(self, vec):
        return Vec2d(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):
        return Vec2d(self.x - vec.x, self.y - vec.y)

    def __mul__(self, k):
        if isinstance(k, Vec2d):
            return self.x * k.x + self.y * k.y
        return Vec2d(self.x * k, self.y * k)

    def len(self, x):
        return (x.x ** 2 + x.y ** 2) ** .5

    def int_pair(self):
        return (int(self.x), int(self.y))

    def __str__(self):
        return 'x: {}, y: {}'.format(self.x, self.y)

    def __iter__(self):
        return iter([self.x, self.y])


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []
        self.width = 3

    def add_point(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    def set_points(self):
        for i in range(len(self.points)):
            self.points[i] += self.speeds[i]
            if self.points[i].x > SCREEN_DIM[0] or self.points[i].x < 0:
                self.speeds[i] = Vec2d(- self.speeds[i].x, self.speeds[i].y)
            if self.points[i].y > SCREEN_DIM[1] or self.points[i].y < 0:
                self.speeds[i] = Vec2d(self.speeds[i].x, -self.speeds[i].y)

    def draw_points(self, points, width=3, color=(255, 255, 255)):
        if width > self.width:
            self.width = width
        for point in points:
            pygame.draw.circle(gameDisplay, color, point.int_pair(), width)

    def delete_point(self, current_pos):
        current_x, current_y = current_pos
        scope = ((current_x - self.width, current_x + self.width), (current_y - self.width, current_y + self.width))
        for i in range(len(self.points)):
            x, y = self.points[i]
            if scope[0][0] < x < scope[0][1] and scope[1][0] < y < scope[1][1]:
                self.points.pop(i)
                return str(i)
        return 'No point on this position'


class Knot(Polyline):
    def __init__(self, count):
        super().__init__()
        self.count = count

    def add_point(self, point, speed):
        super().add_point(point, speed)
        self.get_knot()

    def set_points(self):
        super().set_points()
        self.get_knot()

    def delete_knot(self, index):
        if index.isdigit():
            index = int(index)
            del self.points[index]

    def get_point(self, base_points, alpha, deg=None):
        if deg is None:
            deg = len(base_points) - 1
        if deg == 0:
            return base_points[0]
        return base_points[deg] * alpha + self.get_point(base_points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points):
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn))
        return res

    def set_steps(self, mark):
        if mark == 'plus':
            self.count += 1
        elif mark == 'minus':
            self.count -= 1 if self.count > 1 else 0

    def draw_points(self, points, width=3, color=(255, 255, 255)):
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color, points[p_n].int_pair(), points[p_n + 1].int_pair(), width)


def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["A", "Create new field"])
    data.append(["Tab", "Switch field"])
    data.append(["Mouse", "Add or Delete point"])
    data.append(["", ""])
    data.append([str(steps), "Default points"])
    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


def draw_string(fact_steps, c_line, all_line):
    font1 = pygame.font.SysFont("courier", 20)
    font2 = pygame.font.SysFont("serif", 20)
    color = (128, 128, 255)
    data = []
    data.append(["Field:", str(c_line + 1)])
    data.append(["All fields:", str(all_line)])
    data.append(["Actual points:", str(fact_steps)])
    gameDisplay.blit(font1.render(
        data[0][0], True, color), (10, 4))  # Active field
    gameDisplay.blit(font2.render(
        data[0][1], True, color), (90, 4))
    gameDisplay.blit(font1.render(
        data[1][0], True, color), (130, 4))  # Number of fields
    gameDisplay.blit(font2.render(
        data[1][1], True, color), (270, 4))
    gameDisplay.blit(font1.render(
        data[2][0], True, color), (490, 4))  # Actual points
    gameDisplay.blit(font2.render(
        data[2][1], True, color), (670, 4))


def switch(current_line, quantity_line, mark):
    if mark == 'tab':
        if current_line == quantity_line - 1:
            return 0
        else:
            return current_line + 1
    elif mark == 'del':
        if current_line == quantity_line or current_line == 0:
            return 0
        else:
            return current_line - 1



if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")
    steps = 25
    working = True
    coro = [[Polyline(), Knot(steps)]]
    show_help = False
    pause = True
    hue = 0
    color = pygame.Color(0)
    c_line = 0
    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    coro[c_line][0] = Polyline()
                    coro[c_line][1] = Knot(steps)
                if event.key == pygame.K_a:
                    steps = 25
                    coro.append([Polyline(), Knot(steps)])
                    c_line = len(coro) - 1
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_TAB:
                    c_line = switch(c_line, len(coro), 'tab')
                if event.key == pygame.K_d:
                    if len(coro) > 1:
                        del coro[c_line]
                        c_line = switch(c_line, len(coro), 'del')
                if event.key == pygame.K_KP_PLUS:
                    coro[c_line][1].set_steps('plus')
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    coro[c_line][1].set_steps('minus')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    coro[c_line][0].add_point(Vec2d(event.pos), Vec2d(random.random() * 2, random.random() * 2))
                    coro[c_line][1].add_point(Vec2d(event.pos), Vec2d(random.random() * 2, random.random() * 2))
                elif event.button == 3 and pause:
                    coro[c_line][1].delete_knot(coro[c_line][0].delete_point(Vec2d(event.pos)))

        gameDisplay.fill((0, 0, 0))
        draw_string(coro[c_line][1].count, c_line, len(coro))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        coro[c_line][0].draw_points(coro[c_line][0].points)
        coro[c_line][1].draw_points(coro[c_line][1].get_knot(), 3, color)
        if not pause:
            coro[c_line][0].set_points()
            coro[c_line][1].set_points()
        if show_help:
            draw_help()
        pygame.display.flip()
    pygame.display.quit()
    pygame.quit()
    exit(0)
