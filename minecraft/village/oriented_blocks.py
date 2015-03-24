from building import BuildingBlock
import mcpi.block as block
from mcpi.vec3 import Vec3

class OrientedBlock(BuildingBlock):
	def __init__(self, north=None, south=None, east=None, west=None, *args, **kwargs):
		super(OrientedBlock, self).__init__(*args, **kwargs)
		self.NORTH = north
		self.SOUTH = south
		self.EAST = east
		self.WEST = west
		
	def rotateLeft(self):  
		super(OrientedBlock, self).rotateLeft()
		
		if self.data == self.EAST:	
			self.data = self.NORTH
		elif self.data == self.SOUTH:
			self.data == self.EAST
		elif self.data == self.WEST:
			self.data = self.SOUTH
		else:
			self.data = self.WEST
		
	
	def rotateRight(self, ct=1): 
		for i in range(ct):	
			self.pos.rotateRight()
			self.pos2.rotateRight()

			if self.data == self.EAST:	
				self.data = self.SOUTH
			elif self.data == self.SOUTH:
				self.data == self.WEST
			elif self.data == self.WEST:
				self.data = self.NORTH
			else:
				self.data = self.EAST

class Torch(OrientedBlock):
	EAST = 1
	WEST = 2
	SOUTH = 3
	NORTH = 4

	def __init__(self, *args, **kwargs):
		super(Torch, self).__init__(Torch.NORTH, Torch.SOUTH, Torch.EAST, Torch.WEST, *args, **kwargs)
		
class Ladder(OrientedBlock):
	NORTH = 2
	SOUTH = 3
	WEST = 4
	EAST = 5

	def __init__(self, *args, **kwargs):
		super(Ladder, self).__init__(Ladder.NORTH, Ladder.SOUTH, Ladder.EAST, Ladder.WEST, *args, **kwargs)

class Stair(OrientedBlock):
	EAST = 0
	WEST = 1
	SOUTH = 2
	NORTH = 3

	def __init__(self, *args, **kwargs):
		super(Stair, self).__init__(Stair.NORTH, Stair.SOUTH, Stair.EAST, Stair.WEST, *args, **kwargs)

		