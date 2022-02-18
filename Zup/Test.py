#!/bin/env python

import curses
from time import time
from Object import *

keymap = {32: 'Space', 258: 'Down', 259: 'Up', 260: 'Left', 261: 'Right', 113: 'Q', 43: 'Plus', 45: 'Minus', 10: 'Enter', -1: 'Pass'}
keychar = {32: ' ', 258: 'v', 259: '^', 260: '<', 261: '>', 113: 'Q', 43: '+', 45: '-', 10: 'n', -1: ' '}

levelData = [
    (),
    ()
    ]

def clearScreen():
    print(chr(27) + "[2J")

def main(stdscr):
    stdscr.nodelay()
    playing = True
    nextLevel = True
    lvlIndex = -1
    lvlSpeed = 0.200
    moveList = []
    lastFrame = ()
    
