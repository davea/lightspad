#!/usr/bin/env python
"""
Imports the puzzles from the iPhone game Lights Off and stores them in puzzles.json in the current directory.
"""
import sys
import os
import json
try:
    from Foundation import NSDictionary
except ImportError:
    print "Couldn't import Foundation - are you running on OS X? If so, try re-running outside of a virtualenv."
    sys.exit(1)


def main():
    if len(sys.argv) == 1 or not os.path.isfile(sys.argv[1]):
        print "Please specify the puzzles.plist file path."
        return
    puzzles = []
    for puzzlestring in NSDictionary.dictionaryWithContentsOfFile_(sys.argv[1])['puzzles']:
        puzzle = []
        for i, c in enumerate(puzzlestring):
            x = i%5
            y = 4-(i/5) # Y coordinate is flipped
            if c == "x":
                puzzle.append((x, y))
        puzzles.append(puzzle)
    with open("puzzles.json", 'w') as f:
        f.write(json.dumps(puzzles))
        print "Wrote puzzles.json"

if __name__ == '__main__':
    main()