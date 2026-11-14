# --- Imports ---
from random import randrange
from actor import Actor, Arena, Point
from Wall1 import Wall, LWall, WWall, Bomb, Door
from Ballom import Ballom
from Bomberman import Bomberman, BombermanDeath
from Explosion import Center_exp
import g2d


# --- Constants ---
TILE = 16
STEP = 1


# --- Global Variables ---
game_time = 351  
points = 0
finish = False
Win = False
x = y = 0
zz = 0
clock = 0


# --- Utility Functions ---
def is_valid_position(pos, arena, bomberman_pos):
    x, y = pos
    for actor in arena.actors():
        ax, ay = actor.pos()
        aw, ah = actor.size()
        if ax <= x < ax + aw and ay <= y < ay + ah:
            return False

    if x < TILE or x >= 512 - TILE or y < TILE * 2 or y >= 224 - TILE:
        return False
    bx, by = bomberman_pos
    if abs(x - bx) <= TILE and abs(y - by) <= TILE:
        return False
    return True


def spawn_entity(entity_class, count, arena, bounds, bomberman_pos):
    min_x, max_x, min_y, max_y = bounds
    for _ in range(count):
        while True:
            x = randrange(min_x, max_x, TILE)
            y = randrange(min_y, max_y, TILE)
            if is_valid_position((x, y), arena, bomberman_pos):
                arena.spawn(entity_class((x, y)))
                break

# --- Initialization Function ---
def initialize(b):
    global arena
    arena = Arena((512, 224))

# Set up Bomberman
    b._x, b._y = (16, 32)
    b._bomb_active = False
    b._bomb_count = 0
    b._dx, b._dy = 0, 0  
    b._alive = True  
    b._lifechange = False 
    arena.spawn(b)
    
    # Bomberman initial position
    bomberman_pos = (16, 32)
    # Spawn boundary walls
    for i in range(224 // TILE):
        arena.spawn(WWall((0, i * TILE + TILE)))  # Left boundary
        arena.spawn(WWall((512 - TILE, i * TILE + TILE)))  # Right boundary
    for i in range(512 // TILE):
        arena.spawn(WWall((i * TILE, TILE)))  # Top boundary
        arena.spawn(WWall((i * TILE, 224 - TILE)))  # Bottom boundary

    # Internal walls
    for i in range(1, 16):
        for j in range(1, 6):
            arena.spawn(WWall((32 * i, 32 * j + TILE)))

    # Spawn Balloms, LWall, and Door
    spawn_entity(Ballom, 10, arena, (16, 512 - 16, 32, 224 - 16), bomberman_pos)
    spawn_entity(LWall, 25, arena, (16, 512 - 16, 32, 224 - 16), bomberman_pos)
    for actor in arena.actors():
        if isinstance(actor, LWall):
            x, y = actor.pos()
    arena.spawn(Door((x, y)))


# --- Tick Function ---
def tick():
    import time
    global game_time, b, clock, points, finish, arena, Win, x, y, zz, last_offset_x

    bool = True  
    flag = False
    k = False

    if 'last_offset_x' not in globals():
        last_offset_x = 0  # Initialize camera offset 
     
    # Update points for Ballom death
    for a in arena.actors():        
        if isinstance(a, Ballom):
            if a._flag == 7 and a._frame % 4 == 3:
                points += 100
    
    # Check for Ballom presence
    for a in arena.actors():        
        if isinstance(a, Ballom):        
            
            k = True

    # Open Door if no Balloms are left
    for a in arena.actors():        
        if isinstance(a, Door) and k == False:
            a._closed = False
            x, y = a.pos()
            finish = True

    # Check if Bomberman reaches the Door
    for actor in arena.actors():
        if isinstance(actor, Bomberman) and actor._x == x and actor._y == y:
            Win = True

    # Check if Bomberman is alive
    for actor in arena.actors():
        if isinstance(actor, (BombermanDeath, Bomberman)):
            bool = False          

    # Respawn Bomberman if needed
    if bool and b._lives >= 0:
        flag = True
        clock = 40
        initialize(b)
        game_time = 351
        
    # Load images
    img2 = "death screen.jpeg"
    img = "bomberman.png"
    img3 = "end_screen.png"
    img4 = "game_over.jpg" 
    offset_x = last_offset_x

    
    # Game states
    if b._lives == 0 or game_time == 0:
        g2d.clear_canvas()
        g2d.draw_image (img4,(0, 0),(272, 224))
        


    elif flag or clock != 0:    
        g2d.clear_canvas()
        g2d.draw_image ('death screen.jpeg',(0, 0),(272, 224))
        last_offset_x = 0
        
        clock -= 1
    
    elif Win  :
        # Handle win state
        for a in arena.actors():
            if not isinstance(a, Bomberman):
                arena.kill(a)
        g2d.clear_canvas()
        if zz == 0:        

            arena = Arena((512, 224))
            b._x,b._y = (272/2,224/2)
            arena.spawn(b) 
            zz = 1

        b._bomb_active = True
        b._alive = True   
               
        g2d.draw_image (img3,(0, 0),(272, 224))
        g2d.draw_image(img, (b._x , b._y), b.sprite(), b.size())
        
        

        
        arena.tick(g2d.current_keys())
                    
    
    else: 
        # Update game board
        if arena.count() % 40 == 0 and game_time > 0:
            game_time -= 1
        g2d.clear_canvas()
        # Draw game elements
        g2d.set_color((0, 150, 0))
        g2d.draw_rect((0, 16), (512, 208 - 16))
        g2d.set_color((127, 127, 127))
        g2d.draw_rect((0, 0), (512, 16))
        for actor in arena.actors():
            if isinstance(actor, Bomberman):
                bx, _ = actor.pos()
                if bx > 136:  
                    offset_x = min(bx - 136, 512 - 272)
                    last_offset_x = offset_x
            

        for a in arena.actors():
            if isinstance(a, Door):
                ax, ay = a.pos()
                sprite = a.sprite()
                size = a.size()
                g2d.draw_image(img, (ax - offset_x, ay), sprite, size)
        for a in arena.actors():
            if isinstance(a, Center_exp):
                ax, ay = a.pos()
                sprite = a.sprite()
                size = a.size()
                g2d.draw_image(img, (ax - offset_x, ay), sprite, size)
                
        for a in arena.actors():    
            if isinstance(a, Ballom):
                ax, ay = a.pos()
                sprite = a.sprite()
                size = a.size()
                g2d.draw_image(img, (ax - offset_x, ay), sprite, size)

        
        for a in arena.actors():
            if not isinstance(a, Center_exp) and not isinstance(a, Ballom)and not isinstance(a, Door):
                ax, ay = a.pos()
                sprite = a.sprite()
                size = a.size()
                g2d.draw_image(img, (ax - offset_x, ay), sprite, size)
    
            
        # Display timer, points and lives
        g2d.set_color((255, 255, 255))  
        timer_text = f"TIME {game_time:02d}"  
        g2d.draw_text(timer_text, (30, 9), 10)        
        
        g2d.set_color((255, 255, 255))
        text = f"LEFT {b._lives}"
        g2d.draw_text(text, (250, 9), 10)

        g2d.set_color((255, 255, 255))
        text = f"{points}"
        g2d.draw_text(text, (125, 9), 10)
        
        arena.tick(g2d.current_keys())


# --- Main Function ---
def main():
    global b
    g2d.init_canvas((272, 224), 2.5)
    


    b = Bomberman((16, 32))
    initialize(b)
    
    
    g2d.main_loop(tick, 40)

# --- Entry Point ---
if __name__ == "__main__":
    main()
