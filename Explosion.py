# --- Imports ---
from random import choice, randrange
from actor import Actor, Arena, Point


# --- Constants ---
TILE = 16
STEP = 1

# --- Base Class for Explosion (Center_exp) ---
class Center_exp(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = TILE, TILE
        self._frame = 1
        self._finished= False
    def move (self,arena: Arena):
        # Increment frame and check if the explosion animation should end
        self._frame += 1
        if self._frame > 16:
            arena.kill(self)
     
    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h
    
    def sprite(self):
        # Define the sprite based on frame animation
        if self._frame // 3 % 6 == 0:
            return 32, 96
        elif self._frame // 3 % 6 == 1 :
            return 112, 96
        elif self._frame // 3 % 6 == 2 :
            return 32, 176
        elif self._frame // 3 % 6 == 3 :
            return 112, 176 
        elif self._frame // 3 % 6 == 4 :
            return 32,176
        elif self._frame // 3 % 6 == 5 :
            return 112, 96

# Derived Explosion Classes for Left, Right, Up, Down        
class Left_exp(Center_exp):

    def sprite(self):
        if self._frame // 3 % 6 == 0 :
            return 0, 96
        elif self._frame // 3 % 6 == 1 :
            return 80, 96
        elif self._frame // 3 % 6 == 2 :
            return 0, 176
        elif self._frame // 3 % 6 == 3 :
            return 80, 176 
        elif self._frame // 3 % 6== 4 :
            return 0,176
        elif self._frame // 3 % 6== 5 :
            return 80, 96
            
class Right_exp(Center_exp):

    def sprite(self):
        if self._frame // 3 % 6== 0  :
            return 32+ 32, 96 
        elif self._frame // 3 % 6== 1 :
            return 112 + 32, 96 
        elif self._frame // 3 % 6== 2 :
            return 32+ 32, 176 
        elif self._frame // 3 % 6 == 3 :
            return 112 + 32, 176 
        elif self._frame // 3 % 6 == 4 :
            return 32 + 32, 176 
        elif self._frame // 3 % 6== 5 :
            return 112 + 32, 96 
        
class Up_exp(Center_exp):
 
    def sprite(self):
        if self._frame // 3 % 6 == 0 :
            return 32, 96 + 32
        elif self._frame // 3 % 6 == 1 :
            return 112, 96 + 32
        elif self._frame // 3 % 6 == 2 :
            return 32, 176 + 32
        elif self._frame // 3 % 6 == 3 :
            return 112, 176 + 32
        elif self._frame // 3 % 6 == 4 :
            return 32,176 + 32
        elif self._frame // 3 % 6 == 5 :
            return 112, 96 + 32   
class Down_exp(Center_exp):

    def sprite(self):
        if self._frame // 3 % 6 == 0 :
            return 32, 96 - 32
        elif self._frame // 3 % 6 == 1 :
            return 112, 96 - 32
        elif self._frame // 3 % 6 == 2 :
            return 32, 176 - 32
        elif self._frame // 3 % 6 == 3 :
            return 112, 176 - 32
        elif self._frame // 3 % 6 == 4 :
            return 32,176 - 32
        elif self._frame // 3 % 6 == 5 :
            return 112, 96 - 32      
