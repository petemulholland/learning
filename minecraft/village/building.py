from mcpi.vec3 import Vec3
import mcpi.block as block
import time

RELATIVE_OFFSET = Vec3(0,0,2)

class BuildingBlock():
	def __init__(self, offset, pos, block_type=block.AIR, pos2=None, data=0):
		self.offset = offset
		self.pos = pos
		self.block = block_type
		self.pos2 = pos2
		self.data = data
	
	def clone(self):
		new_offset = self.offset.clone()
		new_pos = self.pos.clone()
		new_pos2 = None
		if self.pos2 is not None:
			new_pos2 = self.pos2.clone()
		return BuildingBlock(new_offset, new_pos, 
							 self.block, new_pos2, self.data)

	def applyRelativeOffset(self, offset):
		self.pos += offset
		if self.pos2 is not None:
			self.pos2 += offset

	def rotateLeft(self):  
		self.pos.rotateLeft()
		if self.pos2 is not None:
			self.pos2.rotateLeft()
	
	def rotateRight(self, ct=1): 
		for i in range(ct):	
			self.pos.rotateRight()
			if self.pos2 is not None:
				self.pos2.rotateRight()
	
	def set_level(self, y):
		self.pos.y = y
		if self.pos2 is not None:
			self.pos2.y = y

	def _build(self, mc, blockType):
		p1 = self.offset + self.pos
		if self.pos2 is None:
			mc.setBlock(p1.x, p1.y, p1.z, blockType, self.data)
		else:
			p2 = self.offset + self.pos2
			mc.setBlocks(p1.x, p1.y, p1.z, 
						 p2.x, p2.y, p2.z, blockType, self.data)

	def build(self, mc):
		self._build(mc, self.block)
		
	def clear(self, mc, fill=block.AIR):
		self._build(mc, fill)

class BuildingLayer():
	def __init__(self, blocks=[], level=0):
		self.blocks = []
		self._level = level
		for block in blocks:
			new_block = block.clone()
			new_block.set_level(level)
			self.blocks.append(new_block)
		
	def clone(self):
		blocks = []
		for block in self.blocks:
			blocks.append(block.clone())
		return BuildingLayer(blocks)

	@property 
	def level(self): 
		'''level attribute accessor'''
		return self._level 
	
	@level.setter 
	def level(self, y): 
		self._level = y
		for block in self.blocks:
			block.set_level(y)
			
	def applyRelativeOffset(self, offset):
		for block in self.blocks:
			block.applyRelativeOffset(offset)
		
	def offsetAndRotateLeft(self, offset):
		for block in self.blocks:
			block.applyRelativeOffset(offset)
			block.rotateLeft()
			
	def rotateLeft(self):  
		for block in self.blocks:
			block.rotateLeft()
	
	def offsetAndRotateRight(self, offset, ct=1): 
		for block in self.blocks:
			block.applyRelativeOffset(offset)
			block.rotateRight(ct)

	def rotateRight(self, ct=1): 
		for block in self.blocks:
			block.rotateRight(ct)
				
	def build(self, mc):
		for block in self.blocks:
			block.build(mc)
		
	def clear(self, mc, fill=block.AIR):
		for block in self.blocks:
			block.clear(mc, fill)
	
class Building(object):
	NORTH = 0
	SOUTH = 2
	EAST  = 1
	WEST  = -1

	def __init__(self, position=Vec3(0,0,0), direction=NORTH):
		self.pos = position
		self.dir = direction
		self.layers = []

	def _get_relative_offset(self):
		return RELATIVE_OFFSET
	
	def _set_direction(self):
		rel_offset = self._get_relative_offset()
		for layer in self.layers:
			if self.dir == Building.WEST:
				if rel_offset is not None:
					layer.offsetAndRotateLeft(rel_offset)
				else:
					layer.rotateLeft()
			elif self.dir == Building.EAST:
				if rel_offset is not None:
					layer.offsetAndRotateRight(rel_offset)
				else:
					layer.rotateRight()
			elif self.dir == Building.SOUTH:
				if rel_offset is not None:
					layer.offsetAndRotateRight(rel_offset, 2)
				else:
					layer.rotateRight(2)

	def clear(self, mc, ground_fill=block.DIRT, debug=True):
		if debug == True:
			self._clear_layers_down(mc)
			
		for i in xrange(len(self.layers) - 1, 0, -1):
			if self.layers[i].level < 0:
				self.layers[i].clear(mc, ground_fill)
				if debug == True:
					time.sleep(1)
			else:
				self.layers[i].clear(mc) # default to AIR
			time.sleep(1)
	
	def _clear_layers_down(self, mc):
		for i in xrange(len(self.layers) - 1, 0, -1):
			self.layers[i].clear(mc)
			time.sleep(1)
		
	def build(self, mc, debug=True):
		if debug == True:
			self._clear_layers_down(mc)
		
		for layer in self.layers:
			layer.build(mc)
			if debug == True:
				time.sleep(1)
			
		
			