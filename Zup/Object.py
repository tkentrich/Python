from random import random
from Misc import XY, Direction, Up, Down, Left, Right, Neutral

class Thing:
    def __init__(self):
        self._name = "Undefined Thing"
        self._char = "?"
        self._passable = False
        
    def char(self):
        return self._char

class Brick(Thing):
    def __init__(self):
        Thing.__init__(self)
        self._name = "Brick"
        self._char = "X"
        
class Block(Thing):
    def __init__(self):
        Thing.__init__(self)
        self._name = "Block"
        self._char = "="
        
class Exit(Thing):
    def __init__(self):
        Thing.__init__(self)
        self._name = "Exit"
        self._char = "O"
        self._passable = True

class Player(Thing):
    def __init__(self):
        Thing.__init__(self)
        self._name = "Player"
        self._passable = True
        self.turn(Neutral)
        
    def turn(self, direction):
        self.direction = direction
        
    def char(self):
        return self.direction.char()

class Level:
    def __init__(self, size):
        self._size = size
        self._objects = [[[] for y in range(0, self._size.y)] for x in range(0, self._size.x)]
        self._hasPlayer = False
        self._focus = self._size
