from building import Building, BuildingEx, BuildingBlock, Torch
from base.fixtures import OpenDoorway
from base.constants import WALL_HEIGHT, EXTERIOR_WALLS, INTERIOR_WALLS
import mcpi.block as block
from mcpi.block import Block
from mcpi.vec3 import Vec3

class GroundRoomBase(BuildingEx):
	''' basic 6x6 (internal) room to base other castle rooms off '''
	WALLS_CORNER_POS = {'South East' : Building.SE_CORNER_POS + Vec3(0,0,0), 
						'South West' : Building.SE_CORNER_POS + Vec3(-7,0,0),
						'North West' : Building.SE_CORNER_POS + Vec3(-7,0,-7),
						'North East' : Building.SE_CORNER_POS + Vec3(0,0,-7) }

	WIDTH = WALLS_CORNER_POS['South East'].x - (WALLS_CORNER_POS['South West'].x - 1)
	#TODO: figure out how to specify block type for each wall
	def __init__(self, *args, **kwargs):
		super(GroundRoomBase, self).__init__(width=GroundRoomBase.WIDTH, *args, **kwargs)

	def _create_structure(self):
		super(GroundRoomBase, self)._create_structure()

		# create walls
		builds = []
		builds.append(BuildingBlock(GroundRoomBase.WALLS_CORNER_POS['South East'],
									EXTERIOR_WALLS, 
									GroundRoomBase.WALLS_CORNER_POS['South West'] + Vec3(0,WALL_HEIGHT,0),
									description="South wall"))
		builds.append(BuildingBlock(GroundRoomBase.WALLS_CORNER_POS['South West'],
									EXTERIOR_WALLS, 
									GroundRoomBase.WALLS_CORNER_POS['North West'] + Vec3(0,WALL_HEIGHT,0),
									description="West wall"))
		builds.append(BuildingBlock(GroundRoomBase.WALLS_CORNER_POS['North East'],
									EXTERIOR_WALLS, 
									GroundRoomBase.WALLS_CORNER_POS['North West'] + Vec3(0,WALL_HEIGHT,0),
									description="North wall"))
		builds.append(BuildingBlock(GroundRoomBase.WALLS_CORNER_POS['South East'],
									EXTERIOR_WALLS, 
									GroundRoomBase.WALLS_CORNER_POS['North East'] + Vec3(0,WALL_HEIGHT,0),
									description="East wall"))

		self._add_section("Base room walls", builds)
		self._add_windows()

	def _add_windows(self):
		builds = []
		builds.append(BuildingBlock(GroundRoomBase.WALLS_CORNER_POS['North East'] + Vec3(-1,1,0),
									block.GLASS_PANE, 
									GroundRoomBase.WALLS_CORNER_POS['North East'] + Vec3(-1,2,0),
									description="window"))
		builds.append(BuildingBlock(GroundRoomBase.WALLS_CORNER_POS['North East'] + Vec3(-3,1,0),
									block.GLASS_PANE, 
									GroundRoomBase.WALLS_CORNER_POS['North East'] + Vec3(-4,2,0),
									description="window"))
		builds.append(BuildingBlock(GroundRoomBase.WALLS_CORNER_POS['North East'] + Vec3(-6,1,0),
									block.GLASS_PANE, 
									GroundRoomBase.WALLS_CORNER_POS['North East'] + Vec3(-6,2,0),
									description="window"))
		builds.append(Torch(GroundRoomBase.WALLS_CORNER_POS['North East'] + Vec3(-2,2,1),
							block.TORCH.withData(Torch.SOUTH)))
		builds.append(Torch(GroundRoomBase.WALLS_CORNER_POS['North West'] + Vec3(2,2,1),
							block.TORCH.withData(Torch.SOUTH)))

		self._add_section("Base room windows", builds)



class UpperRoomBase(GroundRoomBase):
	def __init__(self, *args, **kwargs):
		super(UpperRoomBase, self).__init__(*args, **kwargs)

	def _create_structure(self):
		super(GroundRoomBase, self)._create_structure()
		builds = []
		builds.append(BuildingBlock(UpperRoomBase.WALLS_CORNER_POS['South East'],
									INTERIOR_WALLS, 
									UpperRoomBase.WALLS_CORNER_POS['South West'] + Vec3(0,WALL_HEIGHT,0),
									description="South wall"))
		builds.append(BuildingBlock(UpperRoomBase.WALLS_CORNER_POS['South West'],
									INTERIOR_WALLS, 
									UpperRoomBase.WALLS_CORNER_POS['North West'] + Vec3(0,WALL_HEIGHT,0),
									description="West wall"))
		builds.append(BuildingBlock(UpperRoomBase.WALLS_CORNER_POS['South East'],
									INTERIOR_WALLS, 
									UpperRoomBase.WALLS_CORNER_POS['North East'] + Vec3(0,WALL_HEIGHT,0),
									description="East wall"))
		# add exterior north wll last so corners are last written as exterior.
		builds.append(BuildingBlock(UpperRoomBase.WALLS_CORNER_POS['North East'],
									EXTERIOR_WALLS, 
									UpperRoomBase.WALLS_CORNER_POS['North West'] + Vec3(0,WALL_HEIGHT,0),
									description="North wall"))
		# add doors to south wall

		self._add_section("Upper room walls", builds)
		self._add_windows()
