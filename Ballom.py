# --- Imports ---
from random import choice, randrange
from actor import Actor, Arena, Point
from Wall1 import Wall
from Bomberman import Bomberman
from Explosion import *

# --- Constants ---
TILE = 16
STEP = 1

# --- Ballom Class ---
class Ballom(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._x = self._x // TILE * TILE
        self._y = self._y // TILE * TILE
        self._w, self._h = TILE, TILE
        self._speed = 1 
        self._dx, self._dy = choice([(0, -1), (1, 0), (0, 1), (-1, 0)]) # Random initial movement direction
        self._frame = 0
        self._flag = 0  # Flag for animation state
        self._alive = True  # Alive state
        self._points = 0  # Score points
        
    # Move function to handle Ballom's movement in the arena
    def move(self, arena: Arena):
        if not self._alive:
            self.die(arena)
        else:
            allowed = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Directions Ballom can move

            # Check for collisions with walls and adjust movement accordingly
            for w in arena.collisions():
                if isinstance(w, Wall):
                    wx, wy = w.pos()
                    if wy < self._y and abs(wx - self._x) < TILE:
                        if allowed.count((0, -1)):
                            allowed.remove((0, -1)) # Remove upward movement if blocked
                    elif wy > self._y and abs(wx - self._x) < TILE:
                        if allowed.count((0, 1)):
                            allowed.remove((0, 1)) # Remove downward movement if blocked
                    elif wx > self._x and abs(wy - self._y) < TILE:
                        if allowed.count((1, 0)):
                            allowed.remove((1, 0)) # Remove rightward movement if blocked
                    elif wx < self._x and abs(wy - self._y) < TILE:
                        if allowed.count((-1, 0)):
                            allowed.remove((-1, 0)) # Remove leftward movement if blocked

            # Ballom only changes direction when it is aligned with the grid
            if self._x % (16 // 2) == 0 and self._y % (16 // 2) == 0:
                if len(allowed) > 0:
                    self._dx, self._dy = choice(allowed)# Choose a new direction
                else: 
                    self._dx, self._dy = (0,0) # If no directions are allowed, stop

            # Move the Ballom in the current direction
            self._x += self._dx
            self._y += self._dy

            # Check for collision with Bomberman
            for actor in arena.actors():
                if isinstance(actor, Bomberman):
                    ax, ay = actor.pos()
                    if (self._x // TILE == ax // TILE) and (self._y // TILE == ay // TILE):
                        if actor._alive:
                            actor.die(arena)

             # Check for collisions with explosions            
            for actor in arena.actors():
                if isinstance(actor, Center_exp):
                    exp_x, exp_y = actor.pos()
                    exp_w, exp_h = actor.size()
                    balloon_x, balloon_y = self.pos()
                    balloon_w, balloon_h = self.size()

                    # Check if the Ballom is in the explosion area
                    if (exp_x < balloon_x + balloon_w and
                        exp_x + exp_w > balloon_x and
                        exp_y < balloon_y + balloon_h and
                        exp_y + exp_h > balloon_y):
                        self._alive = False

        self._frame = arena.count() # Update frame count for animation

    # Function to handle Ballom's death animation and removal
    def die(self, arena: Arena):
        
        if self._frame % 4 == 0:
            self._flag += 1
        

        if self._flag == 8:  # After a certain amount of time, remove Ballom

            arena.kill(self)

    # Position, size and sprite functions for Ballom
    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        if self._alive:
            # Sprite calculation based on direction
            if (self._dx, self._dy) == (0, 1) or (self._dx, self._dy) == (-1, 0):
                return 48 + (((self._frame // 4) % 3) * 16), 240
            elif (self._dx, self._dy) == (0, -1) or (self._dx, self._dy) == (1, 0):
                return 0 + (((self._frame // 4) % 3) * 16), 240
            elif (self._dx, self._dy) == (0, 0):
                return 0 + (((self._frame // 4) % 3) * 16), 240
        else:
            # Ballom death animation
            if self._flag < 5:
                return 96 + ((self._flag) % 5) * 16, 240
            else : 
                self._h = 10
                return 116, 334
    
    