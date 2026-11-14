# --- Imports ---
from random import choice, randrange
from actor import Actor, Arena, Point
from Explosion import *
from Wall1 import *


# --- Constants ---
TILE = 16
STEP = 1

# --- Bomberman Class ---
class Bomberman(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._dx, self._dy = 0, 0
        self._w, self._h = TILE, TILE
        self._speed = STEP
        self._frame = 0
        self._direction = 0
        self._alive = True  
        self._bomb_pass = False
        self._slide = 0
        self._lives = 3
        self._lifechange = False
    

    def move(self, arena: Arena):
        if self._alive:  
            # Movement and Collision Variables
            freeway_u = freeway_d = freeway_l = freeway_r = True
            bomb_pass = False
            self._lifechange = False
            # Handle Explosion Collisions
            for a in arena.actors():
                if isinstance(a, (Center_exp, Left_exp, Right_exp, Up_exp, Down_exp)):
                    ax, ay = a.pos()
                    aw, ah = a.size()
                    if (
                        self._x < ax + aw and self._x + self._w > ax and
                        self._y < ay + ah and self._y + self._h > ay
                    ):
                        self.die(arena)
                        return
                    
            # Handle Bomb and Wall Collisions
            for w in arena.collisions():   
                if isinstance(w, Bomb) :
                    wx, wy = w.pos()
                    if abs(self._x - wx) < 16 and abs(self._y - wy) < 16  :
                        bomb_pass = True
               
            for w in arena.collisions(): 
                wx, wy = w.pos()
                if isinstance(w, Wall) and not isinstance (w, Bomb):
                    
                    if  wy  < self._y and abs(wx - self._x) < 16:
                        freeway_u = False
                    elif  wy >= self._y  and abs(wx - self._x) < 16 :
                        freeway_d = False
                    elif  wx >= self._x  and abs(wy - self._y) < 16:
                        freeway_r = False
                    elif  wx  < self._x and abs(wy - self._y) < 16:
                        freeway_l = False
                    
                if isinstance(w, Bomb) and bomb_pass == False :
                    if  wy  < self._y and abs(wx - self._x) < 16:
                        freeway_u = False
                    elif  wy >= self._y  and abs(wx - self._x) < 16 :
                        freeway_d = False
                    elif  wx >= self._x  and abs(wy - self._y) < 16:
                        freeway_r = False
                    elif  wx  < self._x and abs(wy - self._y) < 16:
                        freeway_l = False

             # Update Movement Based on Keys 
            if self._x % (TILE//6) == 0 and self._y % (TILE//6) == 0:
                self._dx, self._dy = 0, 0
                keys = arena.current_keys()
                
                # Update direction based on keys and collision states
                if "ArrowUp" in keys:
                    if freeway_u:
                        self._dy = -self._speed 
                    else :
                        for w in arena.collisions(): 
                            wx, wy = w.pos()    
                            if isinstance(w, WWall) :
                                if -4 > wx - self._x > -16:
                                    if freeway_r:
                                        self._dx = self._speed
                                elif 4 < wx - self._x < 16:
                                    if freeway_l:    
                                        self._dx = -self._speed
                                else: self._dx, self._dy = (0, 0)
                    self._direction = 0
                    self._frame = arena.count()

                elif "ArrowDown" in keys:
                    if freeway_d:
                        self._dy = self._speed
                    else :
                        for w in arena.collisions(): 
                            wx, wy = w.pos()    
                            if isinstance(w, WWall) :
                                if  -4 > wx - self._x > -16:
                                    if freeway_r:
                                        self._dx = self._speed
                                elif  4 < wx - self._x < 16:
                                    if freeway_l:    
                                        self._dx = -self._speed
                                else: self._dx, self._dy = (0, 0)

                    self._direction = 2
                    self._frame = arena.count()


                elif "ArrowLeft" in keys:
                    if freeway_l:
                        self._dx = -self._speed  
                    else:
                        for w in arena.collisions(): 
                            wx, wy = w.pos()    
                            if isinstance(w, WWall):
                                if   -4 > wy - self._y > -16 :
                                    if freeway_d:
                                        self._dy = self._speed
                                elif  4 < wy - self._y < 16: 
                                    if freeway_u:
                                        self._dy = -self._speed
                                else : self._dx, self._dy = (0, 0)

                    self._direction = 1
                    self._frame = arena.count()


                elif "ArrowRight" in keys:
                    if freeway_r:
                        self._dx = self._speed           
                    else : 
                        for w in arena.collisions(): 
                            wx, wy = w.pos()    
                            if isinstance(w, WWall) :                                
                                if   -4 > wy - self._y > -16:
                                    if freeway_d:
                                        self._dy = self._speed 
                                elif  4 < wy - self._y < 16: 
                                    if freeway_u:
                                        self._dy = -self._speed
                                else : self._dx, self._dy = (0, 0)
                                
                                
                    self._direction = 3
                    self._frame = arena.count()


                count = 0

                for actor in arena.actors():
                    if  isinstance(actor, Bomb):
                        count  = 1 
                        

                # Handle Bomb Placement
                if "x" in keys and count == 0 :                     
                    
                    if 0 < self._x % TILE < 8 :
                        arena.spawn(Bomb(((self._x // TILE) * TILE, (self._y // TILE) * TILE)))
                        self._bomb_active = True
                    elif self._x % TILE >= 8 :
                        arena.spawn(Bomb((((self._x // TILE) * TILE) + TILE, (self._y // TILE) * TILE )))
                        self._bomb_active = True 
                    elif self._y % TILE >= 8 :
                        arena.spawn(Bomb((((self._x // TILE) * TILE) , ((self._y // TILE) * TILE)+16 )))
                        self._bomb_active = True   
                    elif 0 < self._y % TILE < 8 :                   
                        arena.spawn(Bomb(((self._x // TILE) * TILE, (self._y // TILE) * TILE )))
                        self._bomb_active = True
                    elif self._x % 16 == 0 and self._y % 16 == 0:
                        arena.spawn(Bomb(((self._x // TILE) * TILE, (self._y // TILE) * TILE )))
                        self._bomb_active = True

                        

            # Update Position
            self._x += self._dx
            self._y += self._dy
            

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        # Sprite calculation based on direction
        if self._direction == 0 :
            return 48 + (((self._frame // 4) % 3) * 16), 16
        elif self._direction == 1 :
            return 0 + (((self._frame // 4) % 3) * 16), 0
        elif self._direction == 2 :
            return 48 + (((self._frame // 4) % 3) * 16), 0
        elif self._direction == 3 :
            return 0 + (((self._frame // 4) % 3) * 16), 16
        
    def die(self, arena: Arena):

        if self._alive:
            self._alive = False
            self._lives -= 1


            arena.spawn(BombermanDeath(self))
            
            arena.kill(self) 
                       
            print(f"Bomberman has died. Lives left: {self._lives}")
            
            

        

# --- BombermanDeath Class ---      
class BombermanDeath(Actor):
    def __init__(self, man):
        self._x, self._y = man.pos()          
        self._w, self._h = TILE, TILE
        self._frame = 0
        self._flag = False

    def move(self, arena: Arena):
        self._frame += 1



        if self._frame > 20:  
            arena.kill(self)
            
            self._flag = True

        
            
            
            


    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        return self._w, self._h

    def sprite(self) -> Point:
        frame = (self._frame // 3) % 7
        return (frame * 16), 32 

 