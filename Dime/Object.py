
# import copy
from random import random
from Misc import XY, Direction, Up, Down, Left, Right, Neutral

class Object(object):
	def __init__(self):
		self._name = "Unknown Object"
		self._char = ['?']
		self.pushable = False
		self.steady = True
		self.fallInertia = -1
		self.collectible = False
		self.destructible = True
		self.explosive = False
		self._animIndex = int(random() * 100)

	def name(self):
		return self._name

	def char(self):
		self._animIndex %= len(self._char)
		return self._char[self._animIndex]

	def advance(self):
		self._animIndex += 1

class Explosion(Object):
	def __init__(self, intoDiamonds):
		super(Explosion, self).__init__()
		self._name = "Explosion"
		self._char = [' ', 'o', '*']
		self._animIndex = 0
		self.intoDiamonds = intoDiamonds
		self.finished = False

	def char(self):
		if self._animIndex >= len(self._char):
			self.finished = True
			return ' '
		return self._char[self._animIndex]

	def advance(self):
		self._animIndex += 1
		if self._animIndex >= len(self._char):
			self.finished = True

class Steel(Object):
	def __init__(self):
		super(Steel, self).__init__()
		self._name = "Steel"
		self._char = ['+']
		self.destructible = False

class Brick(Object):
	def __init__(self):
		super(Brick, self).__init__()
		self._name = "Brick"
		self._char = ['=']
		self.steady = False

class Rock(Object):
	def __init__(self):
		super(Rock, self).__init__()
		self._name = "Rock"
		self._char = ['O']
		self.fallInertia = 0
		self.steady = False
		self.pushable = True # Copied in, Level just checked isinstance(self, Rock) rather than using pushable. This was defined in Object though...

class Diamond(Object):
	def __init__(self):
		super(Diamond, self).__init__()
		self._name = "Diamond"
		self._char = ["$"]
		self.collectible = True
		self.fallInertia = 0
		self.steady = False

class Dirt(Object):
	def __init__(self):
		super(Dirt, self).__init__()
		self._name = "Dirt"
		self._char = ['.']
		self.collectible = True

class Exit(Object):
	def __init__(self):
		super(Exit, self).__init__()
		self._name = "Locked Exit"
		self._char = ['+']

	def open(self):
		self._name = "Open Exit"
		self._char = ['#']
		self.collectible = True

class Creature(Object):
	def __init__(self):
		super(Creature, self).__init__()
		self._name = "Unknown Creature"
		self._char = ['?']
		self.explosive = True
		self.intoDiamonds = False
		self.direction = Up
		self.moves = [Right, Up, Left, Down]

class Firefly(Creature):
	def __init__(self):
		super(Firefly, self).__init__()
		self._name = "Firefly"
		self._char = ['V', 'V', 'v', 'V', 'V', 'V', 'v']

class Butterfly(Creature):
	def __init__(self):
		super(Butterfly, self).__init__()
		self._name = "Butterfly"
		self._char = ['X', 'X', '|', 'X', '|']
		self.intoDiamonds = True
		self.moves = [Left, Up, Right, Down]

class Player(Object):
	def __init__(self):
		super(Player, self).__init__()
		self._name = "Player"
		self.turn(Neutral)
		self.explosive = True
		self.intoDiamonds = True

	def turn(self, direction):
		self.direction = direction

	def char(self):
		return self.direction.char()

	def advance(self):
		pass

class Level(object):
	Init = 000
	Build = 100
	Waiting = 200
	Running = 201
	Complete = 300
	PlayerDead = 400

	def __init__(self, size):
		self.status = Level.Init
		self.size = size
		self.objects = [[[] for y in range(0, self.size.y)] for x in range(0, self.size.x)]
		self._objectLocations = {}
		self.status = Level.Build
		self.hasPlayer = False
		self.focus = XY(5,5)
		self.message = []
		self.diamonds = 0
		self.diamondsNeeded = 0
		self.frame = 0

	def getChar(self, pos):
		char = ' '
		if pos.x >= 0 and pos.y >= 0 and pos.x < self.size.x and pos.y < self.size.y:
			for obj in self.objects[pos.x][pos.y][:]:
				char = obj.char()
		return char

	def objectLocation(self, obj):
		if obj in self._objectLocations.keys():
			return self._objectLocations[obj]
		return None

	def empty(self, pos):
		return len(self.objects[pos.x][pos.y]) == 0

	def showLevel(self, stdscr):
		stdscr.clear()
		scsz = 10
		for y in range(-scsz, scsz + 1):
			for x in range(-scsz, scsz + 1):
				stdscr.move(y + scsz, x + scsz)
				stdscr.addstr(self.getChar(XY(self.focus.x + x, self.focus.y - y)))
		stdscr.move(scsz * 2 + 2, 0)
		stdscr.addstr("Diamonds: {0}\n".format(self.diamonds))
		for msg in self.message:
			stdscr.addstr(str(msg + "\n"))

	def printLevel(self):
		for y in reversed(range(0, self.size.y)):
			for x in range(0, self.size.x):
				print(self.getChar(XY(x, y)),)
			print()

	def addObject(self, obj, pos):
		self.objects[pos.x][pos.y].append(obj)
		self._objectLocations[obj] = pos
		if not self.hasPlayer and isinstance(obj, Player):
			self.hasPlayer = True
			self.player = obj
			self.focus = pos

	def moveObject(self, obj, pos):
		origPos = self.objectLocation(obj)
		try:
			self.objects[origPos.x][origPos.y].remove(obj)
		except:
			pass
		if isinstance(obj, Player):
			self.focus = pos
		elif isinstance(obj, Creature) and pos == self.focus:
			self.explode(pos)
			return
		self.addObject(obj, pos)

	def surround(self):
		for x in range(0, self.size.x):
			self.addObject(Steel(), XY(x, 0))
			self.addObject(Steel(), XY(x, self.size.y - 1))
		for y in range(1, self.size.y - 1):
			self.addObject(Steel(), XY(0, y))
			self.addObject(Steel(), XY(self.size.x - 1, y))

	def startLevel(self):
		if self.hasPlayer and self.status < Level.Waiting:
			self.status = Level.Waiting

	def move(self, direction):
		if not self.hasPlayer and self.status != Level.PlayerDead:
			return None
		self.frame += 1
		if not self.hasPlayer:
			return
		self.player.turn(direction)
		pos = self.objectLocation(self.player)
		dest = pos + direction
		canMove = True
		for obj in self.objects[dest.x][dest.y][:]:
			if obj.collectible:
				continue
			if obj.pushable and self.empty(dest + direction):
				continue
			canMove = False
			if isinstance(obj, Creature):
				self.explode(pos)
		if canMove:
			for stepOn in self.objects[dest.x][dest.y][:]:
				if obj.collectible:
					self.collect(stepOn)
				if obj.pushable:
					self.moveObject(stepOn, dest + direction)
			self.moveObject(self.player, dest)
		self.moveCreatures()
		self.gravity()
		self.advanceAnimations()

	def removeObject(self, obj):
		pos = self.objectLocation(obj)
		if pos == None:
			self.message.append("Tried to remove " + obj.name())
		if isinstance(obj, Player):
			self.hasPlayer = False
			self.status = Level.PlayerDead
		try:
			self._objectLocations.pop(obj)
		except:
			pass
		if isinstance(pos, XY):
			self.objects[pos.x][pos.y].remove(obj)

	def collect(self, obj):
		if isinstance(obj, Diamond):
			self.diamonds += 1
			if self.diamonds == self.diamondsNeeded:
				self.openExits()
		elif isinstance(obj, Exit):
			self.status = Level.Complete
		self.removeObject(obj)

	def explode(self, pos):
		exploder = None
		for obj in self.objects[pos.x][pos.y][:]:
			if obj.explosive:
				exploder = obj
		if exploder == None:
			self.message.append("Tried to explode at " + str(pos) + ", no exploder")
			return None
		intoDiamonds = exploder.intoDiamonds
		for x in range(pos.x - 1, pos.x + 2):
			for y in range(pos.y - 1, pos.y + 2):
				boom = True
				for obj in self.objects[x][y][:]:
					if obj.destructible:
						self.removeObject(obj)
					elif isinstance(obj, Explosion):
						obj.intoDiamonds = intoDiamonds or obj.intoDiamonds
						boom = False
					else:
						boom = False
				if boom:
					self.addObject(Explosion(intoDiamonds), XY(x, y))

	def advanceAnimations(self):
		for x in range(0, self.size.x):
			for y in range(0, self.size.y):
				for obj in self.objects[x][y][:]:
					obj.advance()
					if isinstance(obj, Explosion):
						if obj.finished:
							self.removeObject(obj)
							if obj.intoDiamonds:
								self.addObject(Diamond(), XY(x, y))

	def openExits(self):
		for x in range(0, self.size.x):
			for y in range(0, self.size.y):
				for obj in self.objects[x][y][:]:
					if isinstance(obj, Exit):
						obj.open()

	def moveCreatures(self):
		creatures = []
		for y in range(0, self.size.y):
			for x in range(0, self.size.x):
				for obj in self.objects[x][y][:]:
					if isinstance(obj, Creature):
						creatures.append(obj)
		creatureMove = {}
		for creature in creatures:
			pos = self.objectLocation(creature)
			creatureMove[creature] = None
			list = creature.moves
			if not creature.direction in list:
				creature.direction = list[1]
			while creature.direction != list[1]:
				list.append(list.pop(0))
			for move in list:
				if self.empty(pos + move):
					creatureMove[creature] = move
					break
			for move in list:
				if pos + move == self.objectLocation(self.player):
					creatureMove[creature] = move
		for creature in creatureMove.keys():
			pos = self.objectLocation(creature)
			dest = pos + creatureMove[creature]
			if self.empty(dest) or dest == self.objectLocation(self.player):
				self.moveObject(creature, dest)
				creature.direction = creatureMove[creature]

	def gravity(self):
		if self.status < Level.Waiting or self.status >= Level.Complete:
			return None
		self.status = Level.Running
		for y in range(0, self.size.y):
			for x in range(0, self.size.x):
				for obj in self.objects[x][y][:]:
					if obj.fallInertia <= -1:
						continue
					below = XY(x, y) + Down
					if self.empty(below) and obj.fallInertia > 0:
						self.moveObject(obj, below)
						belowBelow = below + Down
						if not self.empty(belowBelow):
							objBelow = None
							for objsBelow in self.objects[belowBelow.x][belowBelow.y][:]:
								objBelow = objsBelow
							if objBelow != None and objBelow.explosive:
								self.explode(belowBelow)
					elif self.empty(below):
						obj.fallInertia = 1
					else:
						objBelow = None
						for objsBelow in self.objects[below.x][below.y][:]:
							objBelow = objsBelow
						if objBelow == None:
							continue
						if obj.fallInertia > 0 and objBelow.explosive:
							self.explode(below)
						elif not objBelow.steady:
							#self.message.append(str(objBelow) + " is not steady!")
							if self.empty(XY(x, y) + Left) and self.empty(XY(x, y) + Left + Down):
								self.moveObject(obj, XY(x, y) + Left)
								obj.fallInertia = 1
							elif self.empty(XY(x, y) + Right) and self.empty(XY(x, y) + Right + Down):
								self.moveObject(obj, XY(x, y) + Right)
								obj.fallInertia = 0 # Will get inertia in next X loop iteration
							else:
								obj.fallInertia = 0
		self.status = Level.Waiting
