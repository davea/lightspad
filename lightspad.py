#!/usr/bin/env python
from collections import defaultdict
import time
from pylaunchpad import launchpad

GRID_WIDTH = GRID_HEIGHT = 5
GRID_ORIGIN_X = 1
GRID_ORIGIN_Y = 1

COLOUR_RED = (3, 0)
COLOUR_GREEN = (0, 3)
COLOUR_ORANGE = (3, 3)
COLOUR_OFF = (0, 0)

LEVELS = [
    [
        (3, 0),
        (2, 1),
        (3, 1),
        (4, 1),
        (1, 2),
        (3, 2),
        (0, 3),
        (1, 3),
        (2, 3),
        (1, 4),
    ],
    [
        (0, 0),
        (1, 0),
        (3, 0),
        (4, 0),
        (0, 1),
        (4, 1),
        (0, 3),
        (4, 3),
        (0, 4),
        (1, 4),
        (3, 4),
        (4, 4),
    ]
]


class LightsPadGame(object):
    on_colour = COLOUR_GREEN
    off_colour = COLOUR_OFF
    tick_rate = 20
    
    grid = None
    launchpad = None
    
    def __init__(self, level):
        self.launchpad = launchpad.launchpad(*launchpad.findLaunchpads()[0])
        self.reset_game()
        self.load_level(level)
        
    def run(self):
        while True:
            self.tick()
            time.sleep(1.0/self.tick_rate)
    
    def tick(self):
        while True:
            event = self.launchpad.poll()
            if event is None:
                break
            x, y, pressed = event
            if pressed:
                self.grid_pressed(self.to_grid_x(x), self.to_grid_y(y))
                self.draw_grid()
    
    def load_level(self, level):
        for x, y in level:
            self.grid[x][y] = True
        self.draw_grid()
    
    def grid_pressed(self, x, y):
        if not self.position_is_valid(x, y):
            return
        for grid_x, grid_y in self.get_neighbours(x, y) + [(x, y)]:
            self.grid_toggle(grid_x, grid_y)
    
    def get_neighbours(self, x, y):
        positions = [
            (x-1, y),
            (x+1, y),
            (x, y-1),
            (x, y+1)
        ]
        return [pos for pos in positions if self.position_is_valid(*pos)]
    
    def position_is_valid(self, x, y):
        return x>=0 and y>=0 and x<GRID_WIDTH and y<GRID_HEIGHT
    
    def grid_toggle(self, x, y):
        self.grid[x][y] = not self.grid[x][y]
    
    def draw_grid(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                on = self.grid[x][y]
                colour = self.on_colour if on else self.off_colour
                self.launchpad.light(self.to_launchpad_x(x), self.to_launchpad_y(y), *colour)
    
    def to_launchpad_x(self, x):
        return x + GRID_ORIGIN_X
    
    def to_launchpad_y(self, y):
        return y + GRID_ORIGIN_Y
    
    def to_grid_x(self, x):
        return x - GRID_ORIGIN_X
    
    def to_grid_y(self, y):
        return y - GRID_ORIGIN_Y
    
    def reset_game(self):
        self.grid = defaultdict(lambda: defaultdict(bool))

def main():
    LightsPadGame(LEVELS[0]).run()

if __name__ == '__main__':
    main()