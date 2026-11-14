# --- Imports ---
from random import choice, randrange
from actor import Actor, Arena, Point
from Explosion import *


# --- Constants ---
TILE = 16
STEP = 1

# --- Base Wall Class ---
class Wall(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        self._timer = 48

    def move(self, arena: Arena):
        return

    def pos(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def sprite(self):
        return 80, 48

# Derived Wall Classes: WWall and LWall
class WWall(Wall):
    def sprite(self):
        return 48, 48

class LWall(Wall):
    def __init__(self, pos):
        super().__init__(pos)
        self._exploding = False
        self._frame = 0

    def move(self, arena: Arena):
        if self._exploding:
            self._frame += 1
            if self._frame > 15:
                arena.kill(self)

    def sprite(self) -> Point:
        if self._exploding:
            return 80 + (self._frame // 3 * 16), 48
        else:
            return 64, 48

    def explode(self):
        self._exploding = True
        self._frame = 0

# Bomb Class: Manages bomb behavior and explosions
class Bomb(Wall):
    def __init__(self, pos):
        super().__init__(pos)
        self._timer = 100
        self._owner = None
        
        
    def move(self, arena: Arena):
        self._timer -= 1
        if self._timer <= 0:
            self.explode(arena)

    def explode(self, arena: Arena):
        path_u = path_d = path_r = path_l = True
        x, y = self._x, self._y

        # Create center explosion
        arena.spawn(Center_exp((x, y)))

        # Check collisions and spawn directional explosions
        for w in arena.collisions():
            if isinstance(w, Wall):
                wx, wy = w.pos()

                # Upward explosion
                if wy < self._y and abs(wx - self._x) < 16:
                    path_u = False
                    if isinstance(w, LWall):
                        w.explode()
                else:
                    arena.spawn(Up_exp((x, y + 16)))

                # Downward explosion
                if wy >= self._y and abs(wx - self._x) < 16:
                    path_d = False
                    if isinstance(w, LWall):
                        w.explode()
                else:
                    arena.spawn(Down_exp((x, y - 16)))

                # Rightward explosion
                if wx >= self._x and abs(wy - self._y) < 16:
                    path_r = False
                    if isinstance(w, LWall):
                        w.explode()
                else:
                    arena.spawn(Right_exp((x + 16, y)))

                # Leftward explosion
                if wx < self._x and abs(wy - self._y) < 16:
                    path_l = False
                    if isinstance(w, LWall):
                        w.explode()
                else:
                    arena.spawn(Left_exp((x - 16, y)))

        # Kill the bomb after explosion
        arena.kill(self)
  


    def sprite(self):
        
        frame = (self._timer // 18) % 3
        return (frame * 16, 48)

# Door Class: open/closed
class Door(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        self._closed = True

    def move(self, arena: Arena):
        return

    def pos(self):
        return self._x, self._y

    def size (self):
        return self._w, self._h

    
    def sprite(self):
        if self._closed == True :
            return 176, 48
        elif self._closed == False:
            return 192, 48