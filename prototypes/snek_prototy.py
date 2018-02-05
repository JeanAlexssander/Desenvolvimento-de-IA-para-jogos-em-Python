"""

    ISSO É APENAS UM PROTOTIPO
    NÃO GARANTO QUE NADA DESSE CODIGO SEJA UTILIZADO
    APENAS UM TESTE PARA AVALIAR A PERFORMANCE DE PYTHON
    E TER ALGUMAS BOAS DEFINIÇÕES DE COMO ESTRUTURAR O JOGO

    wasd para movimento
    q para sair
    + para trapacear e crescer

    coisas faltando:
    * implementar obstaculos
    * tratar paredes como obstaculos
    * pontuação
    * Deus
    * interface grafica
    * interface magica
    * ideias boas
    * codigo organizado
    * saber usar DQNs
    * lembrar das belman equations
    * o amor do siraj
"""

class GameOverException(Exception):
    pass


#use python3.6

import random
import os
from getch import getch #pip install getch

WIDTH = 64
HEIGHT = 32



grid = [[0 for i in range(WIDTH)] for j in range(HEIGHT)]



class Snek:
    directions = {
        'w': (0, -1),
        's': (0, 1),
        'd': (1, 0),
        'a': (-1, 0),
    }
    cheats = [
        '+'
    ]
    def __init__(self, x, y):
        self.x, self.y = (x, y)
        self.ate = False
        self.tail = None

    def action(self, c, *args):
        if c in self.directions.keys():
            self.try_moving(c, *args)
        elif c in self.cheats:
            self.cheat_tail()

    def try_moving(self, d, world):
        mx, my = self.directions[d]
        if world.is_game_over(self.x +mx, self.y +my):
            raise GameOverException
        else:
            self.move(d, world)


    def move(self, d, world):
        if self.tail:
            self.tail.advance(self.x, self.y,self.ate, world)
            if self.ate:
                world.update(self.x, self.y, 3)
            else:
                world.update(self.x, self.y, 2)

        else:
            if self.ate:
                self.tail = world.spawn_tail(self.x, self.y)
            else:
                world.update(self.x, self.y, 0)
        self.ate = False
        mx, my = self.directions[d]
        self.x += mx
        self.y += my
        if world.is_food(self.x, self.y):
            self.ate = True
            world.has_food = False
        world.update(self.x, self.y, 1)

    def cheat_tail(self):
        self.ate = True


class Tail:
    def __init__(self, x, y):
        self.x, self.y = (x, y)
        self.tail = None
        self.ate = False

    def advance(self, x, y, ate, world):
        if self.tail:
            self.tail.advance(self.x, self.y, self.ate, world)
        else:
            if self.ate:
                self.ate = False
                self.tail = world.spawn_tail(self.x, self.y)
            else:
                world.update(self.x, self.y, 0)
        self.x = x
        self.y = y
        self.ate = ate



class World:
    key = {
        0: ' ',
        1: '#',
        2: '*',
        3: 'o',
        4: 'f',
    }

    def __init__(self, grid):
        self.grid = grid
        self.has_food = False

    def spawn_snek(self, x, y):
        snek = Snek(x, y)
        self.update(x, y, 1)
        return snek

    def spawn_tail(self, x, y):
        tail = Tail(x, y)
        self.update(x, y, 2)
        return tail

    def spawn_food(self):
        x, y = random.randrange(WIDTH), random.randrange(HEIGHT)
        while self.grid[y][x] == 1:
            x, y = random.randrange(WIDTH), random.randrange(HEIGHT)
        self.update(x, y, 4)
        self.has_food = True

    def is_food(self, x, y):
        return self.grid[y][x] == 4

    def is_snek(self, x, y):
        return self.grid[y][x] in [1,2,3]

    def is_game_over(self, x, y):
        return (x not in range(WIDTH)) or (y not in range(HEIGHT)) or self.is_snek(x, y)

    def update(self, x, y, value):
        """
            maintain the abstraction of x,y for the rest of the code
        """
        self.grid[y][x] = value

    def render(self):
        os.system('clear')
        print('+' + '-'  * WIDTH + '+')
        for line in self.grid:
            line_string = ""
            for n in line:
                line_string += self.key[n]

            print('|'+line_string + '|')
        print('+' + '-'  * WIDTH + '+')

if __name__=='__main__':
    world = World(grid)
    snek = world.spawn_snek(1, 2)
    try:
        while True:
            world.render()
            k = getch()
            if k == 'q':
                break
            snek.action(k, world)
            if not world.has_food:
                world.spawn_food()
    except GameOverException:
        print('Game Over')
