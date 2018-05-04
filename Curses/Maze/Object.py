
class Object(object):
	def __init__(self):
		self._name = "Unknown Object"
		self._char = ['?']
		self._animIndex = 0
		self._passable = False
		self._collectible = False

	def char(self):
		self._animIndex %= len(self._char)
		return self._char[self._animIndex]

	def name(self):
		return str(self._name)

	def advance(self):
		self._animIndex += 1

class Wall(object):
	HORIZONTAL = 1
	VERTICAL = 2
	OTHER = 0
	def __init__(self, wallType = OTHER):
		super(Wall, self).__init__()
		if (wallType == HORIZONTAL):
			self._char = ['-']
		elif (wallType == VERTICAL):
			self._char = ['|']
		else:
			self._char = ['%']

class Exit(object):	
