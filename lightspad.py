#!/usr/bin/env python
from collections import defaultdict
import time
import os
import json
from pylaunchpad import launchpad

GRID_WIDTH = GRID_HEIGHT = 5
GRID_ORIGIN_X = 1
GRID_ORIGIN_Y = 1

COLOUR_RED = (3, 0)
COLOUR_GREEN = (0, 3)
COLOUR_ORANGE = (1, 1)
COLOUR_OFF = (0, 0)

DEFAULT_PUZZLES = [
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
    border_colour = COLOUR_ORANGE
    tick_rate = 20
    
    grid = None
    launchpad = None
    puzzles = None
    current_puzzle = 0
    
    def __init__(self, puzzles):
        self.launchpad = launchpad.launchpad(*launchpad.findLaunchpads()[0])
        self.puzzles = puzzles
        self.draw_border()
        self.start_puzzle()
        
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
    
    def grid_pressed(self, x, y):
        if not self.position_is_valid(x, y):
            if self.position_is_border(x, y):
                self.start_puzzle()
                return
            else:
                return
        for grid_x, grid_y in self.get_neighbours(x, y) + [(x, y)]:
            self.grid_toggle(grid_x, grid_y)
        self.check_puzzle_finished()
    
    def position_is_border(self, x, y):
        return x == -1 or x == GRID_WIDTH or y == -1 or y == GRID_HEIGHT
    
    def check_puzzle_finished(self):
        if self.grid_cleared():
            self.current_puzzle += 1
            self.start_puzzle()
    
    def grid_cleared(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if self.grid[x][y]:
                    return False
        return True
    
    def draw_border(self):
        for x in range(GRID_ORIGIN_X-1, GRID_WIDTH+2):
            for y in range(GRID_ORIGIN_Y-1, GRID_HEIGHT+2):
                if not self.position_is_valid(self.to_grid_x(x), self.to_grid_y(y)):
                    self.launchpad.light(x, y, *self.border_colour)
    
    def draw_start_animation(self):
        self.draw_empty_grid()
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                lx = self.to_launchpad_x(x)
                ly = self.to_launchpad_y(y)
                self.launchpad.light(lx, ly, *COLOUR_RED)
                if x > 0:
                    self.launchpad.light(lx-1, ly, *COLOUR_OFF)
            time.sleep(1.0/8)
    
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
    
    def draw_empty_grid(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                self.launchpad.light(self.to_launchpad_x(x), self.to_launchpad_y(y), *self.off_colour)
        
    
    def to_launchpad_x(self, x):
        return x + GRID_ORIGIN_X
    
    def to_launchpad_y(self, y):
        return y + GRID_ORIGIN_Y
    
    def to_grid_x(self, x):
        return x - GRID_ORIGIN_X
    
    def to_grid_y(self, y):
        return y - GRID_ORIGIN_Y
    
    def start_puzzle(self):
        self.grid = defaultdict(lambda: defaultdict(bool))
        for x, y in self.puzzles[self.current_puzzle]:
            self.grid[x][y] = True
        self.draw_start_animation()
        self.draw_grid()
        


def load_puzzles():
    if not os.path.isfile("puzzles.json"):
        return DEFAULT_PUZZLES
    try:
        with open("puzzles.json", "r") as f:
            print "loaded puzzles.json"
            return json.loads(f.read())
    except:
        print "didn't load puzzles.json"
        return DEFAULT_PUZZLES


def main():
    puzzles = load_puzzles()
    LightsPadGame(puzzles).run()

if __name__ == '__main__':
    main()