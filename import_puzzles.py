#!/usr/bin/env python
"""
Imports the puzzles from the iPhone game Lights Off and stores them in puzzles.json in the current directory.
By default, tries to find the Lights Off .ipa file on disk and load puzzles.plist from the app bundle.
If that can't be found, the puzzles.plist location should be specified on the command line.
"""
import sys
import os
import json
from glob import glob
from zipfile import ZipFile
from tempfile import NamedTemporaryFile
try:
    from Foundation import NSDictionary
except ImportError:
    print "Couldn't import Foundation - are you running on OS X? If so, try re-running outside of a virtualenv."
    sys.exit(1)

def load_puzzles_from_ipa():
    for ipa in glob("/Users/*/Music/iTunes/iTunes*/Mobile Applications/Lights Off*ipa"):
        try:
            z = ZipFile(open(ipa, "r"))
            with NamedTemporaryFile() as f:
                f.write(z.read('Payload/Lights Off.app/puzzles.plist'))
                f.flush()
                print f.name
                return NSDictionary.dictionaryWithContentsOfFile_(f.name)['puzzles']
        except:
            continue
    return None

def load_puzzles():
    if len(sys.argv) == 1:
        puzzles = load_puzzles_from_ipa()
        if not puzzles:
            print "Couldn't find the Lights Off app in your iTunes library. Please specify a valid puzzles.plist file path."
            sys.exit(1)
        return puzzles
    if not os.path.isfile(sys.argv[1]):
        print "Please specify a valid puzzles.plist file path."
        sys.exit(1)
    return NSDictionary.dictionaryWithContentsOfFile_(sys.argv[1])['puzzles']

def main():
    puzzles = []
    for puzzlestring in load_puzzles():
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