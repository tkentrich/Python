#!/usr/bin/env python

import curses
from time import time
from Object import *

keymap = {32: 'Space', 258: 'Down', 259: 'Up', 260: 'Left', 261: 'Right', 113: 'Q', 43: 'Plus', 45: 'Minus', 10: 'Enter', -1: 'Pass'}
keychar = {32: ' ', 258: 'v', 259: '^', 260: '<', 261: '>', 113: 'Q', 43: '+', 45: '-', 10: 'n', -1: ' '}

levelData = [
(3, [
"      O!",
"......=+",
".F   .=$",
".....P=$",
".....==$",
".....+++",
]), 
(6, [
"$+P.O!",
"$++ =+",
"$++ +$",
"$++ +$",
"$++ +$",
"$+. +$",
"$+. +$",
"$+. +$",
"$++ +$",
"+B  +$",
]), 
]

def clearScreen():
	print(chr(27) + "[2J")

def main(stdscr):
	stdscr.nodelay(1)
	playing = True
	nextLevel = True
	lvlIndex = -1
	lvlSpeed = 0.200
	moveList = []
	lastFrame = time() # WAS right before time loop
	while playing:
		if nextLevel:
			nextLevel = False
			lvlIndex += 1
			if lvlIndex >= len(levelData):
				playing = False
			else:
				replay = True
		if replay:
			replay = False
			lvl = buildLevel(levelData[lvlIndex])
			lvl.startLevel()
		lvl.showLevel(stdscr)
		while time() < lastFrame + lvlSpeed:
			pass
		lastFrame = time()
		c = stdscr.getch()
		while c != -1:
			if c in keymap.keys():
				moveList.append(c)
			c = stdscr.getch()
		if len(moveList) > 0:
			move = moveList.pop(0)
			if keymap[move] == 'Space':
				lvl.move(Neutral)
			elif keymap[move] == 'Up':
				lvl.move(Up)
			elif keymap[move] == 'Down':
				lvl.move(Down)
			elif keymap[move] == 'Left':
				lvl.move(Left)
			elif keymap[move] == 'Right':
				lvl.move(Right)
			elif keymap[move] == 'Q':
				playing = False
			elif keymap[move] == 'Plus':
				lvlSpeed /= 2
			elif keymap[move] == 'Minus':
				lvlSpeed *= 2
			elif keymap[move] == 'Enter':
				replay = True
			else:
				lvl.move(Neutral)
		else:
			lvl.move(Neutral)
		lvl.showLevel(stdscr)
		if lvl.status == Level.Complete:
			nextLevel = True
			while stdscr.getch() == -1:
				pass

def buildLevel(levelData):
	strep = levelData[1]
	size = XY(max([len(row) for row in strep]) + 2, len(strep) + 2)
	lvl = Level(size)
	lvl.diamondsNeeded = levelData[0]
	lvl.message.append("Diamonds Needed: " + str(levelData[0]))
	lvl.surround()
	y = size.y - 2
	for row in strep:
		x = 1
		for char in row:
			if char == '=':
				lvl.addObject(Brick(), XY(x, y))
			elif char == '+':
				lvl.addObject(Steel(), XY(x, y))
			elif char == '.':
				lvl.addObject(Dirt(), XY(x, y))
			elif char == 'O':
				lvl.addObject(Rock(), XY(x, y))
			elif char == '!':
				lvl.addObject(Exit(), XY(x, y))
			elif char == '$':
				lvl.addObject(Diamond(), XY(x, y))
			elif char == 'B':
				lvl.addObject(Butterfly(), XY(x, y))
			elif char == 'F':
				lvl.addObject(Firefly(), XY(x, y))
			elif char == 'P':
				lvl.addObject(Player(), XY(x, y))
			x += 1
		y -= 1
	return lvl

if __name__ == '__main__':
	curses.wrapper(main)
