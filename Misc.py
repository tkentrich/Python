

class XY:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __str__(self):
		return "({0}, {1})".format(self.x, self.y)
	def __eq__(self, other):
		if isinstance(other, XY):
			return self.x == other.x and self.y == other.y
		return None
	def __add__(self, other):
		if isinstance(other, XY):
			return XY(self.x + other.x, self.y + other.y)
		elif isinstance(other, Direction):
			return XY(self.x + other.delta.x, self.y + other.delta.y)
		elif other == None:
			return XY(self.x, self.y)
		else:
			return XY(self.x, self.y)

class Direction:
	def __init__(self, delta, char):
		self.delta = delta
		self._char = char
	def char(self):
		return self._char

Up = Direction(XY(0, 1), '^')
Down = Direction(XY(0, -1), 'v')
Left = Direction(XY(-1, 0), '<')
Right = Direction(XY(1, 0), '>')
Neutral = Direction(XY(0, 0), '-')
