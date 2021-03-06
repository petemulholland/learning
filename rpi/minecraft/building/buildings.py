from collections import OrderedDict
from mcpi.vec3 import Vec3
import mcpi.block as mblock
import time
import copy

from functools import wraps 
# according to http://www.tutorialspoint.com/python/time_clock.htm
# time.clock does not include sleep times, only proces times.
# time.time give wall-clock time (or time actually elapsed)
# both appear to return the same timings for apartment block build.
def timethis(func): 
	@wraps(func) 
	def wrapper(*args, **kwargs): 
		start = time.clock()
		r = func(*args, **kwargs) 
		end = time.clock() 
		print '{} - {}.{} : {}'.format(type(args[0]).__name__, func.__module__, func.__name__, end - start)
		return r 
	return wrapper

#wooden pressure plate:
TABLE_TOP = mblock.Block(72)

SLEEP_SECS = 0.1

DEBUG_BLOCK_WRITES = True
DEBUG_BLOCK_CTOR = False
DEBUG_BLOCK_ROTATION = False
DEBUG_LAYERS = False
DISPLAY_BLOCK_DESCRIPTIONS = True

# building apt block overloads bukkit server, (this was down to incorrect data value for carrots, has been corrected) 
DELAY_MULTIPLIER = 0
BLOCK_BUILD_DELAY = 0.05 * DELAY_MULTIPLIER
LAYER_BUILD_DELAY = 0.05 * DELAY_MULTIPLIER # first block wil add another 0.1 to delay
BUILDING_DELAY = 0.1 * DELAY_MULTIPLIER

USE_CONTINUE_PROMPT = False

class BuildingBlock(object):
	def __init__(self, pos, block_type=mblock.AIR, pos2=None, description=None):
		self.pos = pos.clone()
		self.block = block_type
		if pos2 is not None:
			self.pos2 = pos2.clone()
		else:
			self.pos2 = None
		self.description = None
		if DISPLAY_BLOCK_DESCRIPTIONS:
			self.description = description

		if DEBUG_BLOCK_CTOR:
			print str(self)
			
	def __str__(self):
		ret = "Block: pos:{0}".format(str(self.pos))
		ret += ", type:{0}".format(str(self.block))
		if self.pos2 is not None:
			ret += ", pos2:{0}".format(str(self.pos2))
		return ret
		
	def clone(self):
		if DEBUG_BLOCK_CTOR:
			print "Cloning ", str(self) 
		new_pos2 = None
		if self.pos2 is not None:
			new_pos2 = self.pos2.clone()
		return BuildingBlock(self.pos.clone(), self.block.clone(), 
							 new_pos2, self.description)

	def _rotateDescriptionLeft(self):
		# This will probably be very inefficient, so only do when debugging descriptions
		replacements = [("North", "N_orth"), ("north", "n_orth"),
						("East", "North"), ("east", "north"),
						("South", "East"), ("south", "east"),
						("West", "South"), ("west", "south"),
						("N_orth", "West"), ("n_orth", "west")]
		if self.description is not None:
			for old,new in replacements:
				self.description = self.description.replace(old, new)


	def _rotateDescriptionRight(self):
		replacements = [("North", "N_orth"), ("north", "n_orth"),
						("West", "North"), ("west", "north"),
						("South", "West"), ("south", "west"),
						("East", "South"), ("east", "south"),
						("N_orth", "East"), ("n_orth", "East")]
		if self.description is not None:
			for old,new in replacements:
				self.description = self.description.replace(old, new)

	def rotateLeft(self):  
		if DEBUG_BLOCK_ROTATION:
			print "Rotating left", str(self)
		self.pos.rotateLeft()
		if self.pos2 is not None:
			self.pos2.rotateLeft()
		self._rotateDescriptionLeft()
		if DEBUG_BLOCK_ROTATION:
			print "Rotated left", str(self)
	
	def rotateRight(self, ct=1): 
		if DEBUG_BLOCK_ROTATION:
			print "Rotating right ", str(self)
		for i in range(ct):	
			self.pos.rotateRight()
			if self.pos2 is not None:
				self.pos2.rotateRight()
			self._rotateDescriptionRight()
		if DEBUG_BLOCK_ROTATION:
			print "Rotated right", str(self)
	
	def set_level(self, y):
		self.pos.y = y
		if self.pos2 is not None:
			self.pos2.y = y

	def _build(self, mc, pos, block_type):
		time.sleep(BLOCK_BUILD_DELAY)
		p1 = pos + self.pos
		if self.pos2 is None:
			if DEBUG_BLOCK_WRITES:
				out = "setBlock(%s,%s)"%(str(p1), str(block_type))
				if self.description is not None:
					out += " # " + self.description
				print out
			mc.setBlock(p1, block_type)
		else:
			p2 = pos + self.pos2
			if DEBUG_BLOCK_WRITES:
				out = "setBlocks(%s,%s,%s)"%(str(p1), str(p2), str(block_type))
				if self.description is not None:
					out += " # " + self.description
				print out
			mc.setBlocks(p1, p2, block_type)

	def build_at(self, mc, pos):
		self._build(mc, pos, self.block)
		
	def clear_at(self, mc, pos, fill=mblock.AIR):
		self._build(mc, pos, fill)

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
			
	def rotateLeft(self):  
		for block in self.blocks:
			block.rotateLeft()

	def rotateRight(self, ct=1): 
		for block in self.blocks:
			block.rotateRight(ct)
				
	def build_at(self, mc, pos):
		time.sleep(LAYER_BUILD_DELAY)
		for block in self.blocks:
			block.build_at(mc, pos)
		
	def clear_at(self, mc, pos, fill=mblock.AIR):
		time.sleep(LAYER_BUILD_DELAY)
		for blck in reversed(self.blocks):
			blck.clear_at(mc, pos, fill)
	
class Building(object):
	NORTH = 0
	SOUTH = 2
	EAST  = 1
	WEST  = -1

	SE_CORNER_POS = Vec3(0,0,0)

	# TODO: change order of params, width is mandatory, could make orientation default to NORTH
	def __init__(self, orientation, width):
		self.dir = orientation
		self._layers = []
		self._width = width
		self._blocks = [] # building blocks not attached to specific layer, e.g. doors
		self._constructed = False

	def clone(self):
		return type(self)(copy.copy(self.dir))

	@property 
	def width(self): 
		'''width attribute accessor'''
		return self._width 
	
	def add_layer(self, layer):
		self._layers.append(layer)

	def add_block(self, blck):
		self._blocks.append(blck)

	def rotateLeft(self):
		for layer in self._layers:
			layer.rotateLeft()
		for blck in self._blocks:
			blck.rotateLeft()

	def rotateRight(self, ct=1):
		for layer in self._layers:
			layer.rotateRight(ct)
		for blck in self._blocks:
			blck.rotateRight(ct)

	def _set_orientation(self):
		if self.dir == Building.WEST:
			self.rotateLeft()
		elif self.dir == Building.EAST:
			self.rotateRight()
		elif self.dir == Building.SOUTH:
			self.rotateRight(2)

	def _create_structure(self):
		pass

	def construct(self):
		if not self._constructed:
			self._create_structure()
			self._set_orientation()
			self._constructed = True

	def _clear_at(self, mc, pos, ground_fill):
		time.sleep(BUILDING_DELAY)
		self.construct()
		print "clearing down building layers"
		for blck in reversed(self._blocks):
			blck.clear_at(mc, pos, ground_fill)

		for layer in reversed(self._layers):
			if layer.level < 0:
				layer.clear_at(mc, pos, ground_fill)
			else:
				layer.clear_at(mc, pos) # default to AIR

	def clear_to_left(self, mc, pos, ground_fill=mblock.DIRT):
		self._clear_at(mc, pos, ground_fill)

	def clear_to_right(self, mc, pos, ground_fill=mblock.DIRT):
		offset = Vec3(self.width - 1,0,0)
		if self.dir == Building.WEST:		offset.rotateLeft()
		elif self.dir == Building.EAST:		offset.rotateRight()
		elif self.dir == Building.SOUTH:	
			offset.rotateRight()
			offset.rotateRight()

		self._clear_at(mc, pos + offset, ground_fill)

	@timethis
	def build_at(self, mc, pos):
		time.sleep(BUILDING_DELAY)
		self.construct()
		if DEBUG_LAYERS:
			print "building up building layers"
		for layer in self._layers:
			if DEBUG_LAYERS:
				print
				print "building layer: %s"%(layer.level)
			layer.build_at(mc, pos)

		for blck in self._blocks:
			blck.build_at(mc, pos)

	def build_to_left(self, mc, pos):
		print "Building %s to left of %s"%(type(self).__name__, str(pos))
		self.build_at(mc, pos)

	def build_to_right(self, mc, pos):
		print "Building %s to right of %s"%(type(self).__name__, str(pos))
		offset = Vec3(self.width - 1,0,0)
		if self.dir == Building.WEST:		offset.rotateLeft()
		elif self.dir == Building.EAST:		offset.rotateRight()
		elif self.dir == Building.SOUTH:	
			offset.rotateRight()
			offset.rotateRight()

		self.build_at(mc, pos + offset)

class BuildingEx(Building):
	'''This extension to Building maintains an ordered dict of collections of buildable objects
	   so that building sections can be built in order and there's no requirement to 
	   use layers 
	   Buildable objects must implement:
		rotateLeft()
		rotateRight()
		and build_at() ''' 
	def __init__(self, *args, **kwargs):
		super(BuildingEx, self).__init__(*args, **kwargs)
		self._build_sections = OrderedDict()
		self.mirrored = False

	def mirror(self):
		self.mirrored = True

	def _get_x(self, x):
		if self.mirrored:
			return (x * -1) - (self._width - 1)
		else: 
			return x

	def clone(self):
		new_this = type(self)(copy.copy(self.dir))
		new_this.mirrored = copy.copy(self.mirrored)
		for name, data in self._build_sections.items():
			self.add_build_section(name, data)
		return new_this

	def _add_section(self, name, builds):
		self.add_build_section(name, builds)
		del builds[:]

	def add_build_section(self, name, build_objects):
		self._build_sections[name] = copy.copy(build_objects)

	def rotateLeft(self):
		for section in self._build_sections.values():
			for block in section:
				block.rotateLeft()

	def rotateRight(self, ct=1):
		for section in self._build_sections.values():
			for block in section:
				block.rotateRight(ct)

	def construct(self):
		if not self._constructed:
			self._create_structure()
			for name, section in self._build_sections.items():
				for block in section:
					if isinstance(block, (Building, SubBuilding)):
						block.construct()		

			self._set_orientation()
			self._constructed = True

	def _clear_at(self, mc, pos, ground_fill):
		time.sleep(BUILDING_DELAY)
		self.construct()
		print "clearing down building sections"
		for name, section in reversed(self._build_sections.items()):
			print "clearing section: %s"%(name)
			time.sleep(LAYER_BUILD_DELAY)
			for block in section:
				time.sleep(BLOCK_BUILD_DELAY)
				block.clear_at(mc, pos, ground_fill)		

	@timethis
	def build_at(self, mc, pos):
		time.sleep(BUILDING_DELAY)
		self.construct()
		for name, section in self._build_sections.items():
			print "building section: %s"%(name)
			if USE_CONTINUE_PROMPT:
				raw_input("Press enter to build...")
			time.sleep(LAYER_BUILD_DELAY)
			for block in section:
				time.sleep(BLOCK_BUILD_DELAY)
				block.build_at(mc, pos)


class SubBuilding(object):
	def __init__(self, building, pos):
		self.building = building.clone()
		self.pos = pos.clone()

	def rotateLeft(self):
		self.building.rotateLeft()
		self.pos.rotateLeft()

	def rotateRight(self, ct=1):
		self.building.rotateRight(ct)
		for i in range(ct):
			self.pos.rotateRight()

	def construct(self):
		self.building.construct()

	def build_at(self, mc, pos):
		print "Building %s at %s"%(type(self.building).__name__, str(pos + self.pos))
		self.building.build_at(mc, pos + self.pos)
			
