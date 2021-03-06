from building import Building, BuildingEx, BuildingBlock, Torch, Furnace, Chest, Door
from base_room import UpperRoomBase
import mcpi.block as block
from mcpi.block import Block
from mcpi.vec3 import Vec3

class SmeltingRoom(UpperRoomBase):
	def __init__(self, *args, **kwargs):
		super(SmeltingRoom, self).__init__(*args, **kwargs)

	def _create_structure(self):
		super(SmeltingRoom, self)._create_structure()
		builds = []
		builds.append(Door(Door.HINGE_RIGHT, 
							UpperRoomBase.WALLS_CORNER_POS['South East'] + Vec3(-1,0,0),
							block.DOOR_WOOD.withData(Door.SOUTH),
							description="Smelting room door"))
		builds.append(Door(Door.HINGE_LEFT, 
							UpperRoomBase.WALLS_CORNER_POS['South East'] + Vec3(-2,0,0),
							block.DOOR_WOOD.withData(Door.SOUTH),
							description="Smelting room door"))
		self._add_section("Smelting Room Doors", builds)
