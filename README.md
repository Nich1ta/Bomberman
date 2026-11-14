# Bomberman (Python)

A remake of the classic NES *Bomberman* first level, written in Python as a first-year university project (Computer Engineering, University of Parma).

The player moves through a scrolling grid, places bombs to destroy soft walls and enemies (Balloms), and has to find the hidden door to win.

> **Status:** work in progress / paused. The core game is playable.

## Features

- Scrolling camera on a 512×224 map (272×224 viewport, scaled 2.5×)
- Grid-based movement with corner sliding around fixed walls
- Bombs with timed fuse and cross-shaped explosions
- Destructible soft walls with break animation
- Ballom enemies with random movement, death animation and score (+100 each)
- Hidden door under a soft wall, which opens when all enemies are defeated
- Timer, score and lives HUD, with death, game-over and victory screens
- Efficient collision detection using a tile-based spatial grid

## Controls

| Key | Action |
|---|---|
| Arrow keys | Move |
| `X` | Place bomb (one at a time) |

## How to run

Requires **Python 3.10+** and **pygame-ce**.

```bash
pip install pygame-ce
python3 main.py
```

Image files (`bomberman.png`, `death screen.jpeg`, `end_screen.png`, `game_over.jpg`) must be in the same folder as `main.py`.

## Project structure

| File | Contents |
|---|---|
| `main.py` | Game loop, level setup, camera, HUD and game states |
| `Bomberman.py` | Player character and death animation |
| `Ballom.py` | Enemy AI and death animation |
| `Wall1.py` | Fixed walls, soft walls, bombs and door |
| `Explosion.py` | Explosion center and arms |
| `actor.py` | Actor/Arena framework *(course-provided)* |
| `g2d.py` | Simple 2D graphics wrapper on pygame *(course-provided)* |



## Credits

- `actor.py` and `g2d.py`: course framework by [Michele Tomaiuolo](https://tomamic.github.io/), MIT License.
- Sprites based on the original NES *Bomberman* (© Hudson Soft / Konami), used for non-commercial educational purposes only.
