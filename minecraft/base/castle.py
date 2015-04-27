from building import Building, BuildingEx, BuildingBlock, SubBuilding, Torch, Door
from base.constants import *
from base.rooms import *
from base.fixtures import *
from base.enclosure import *
import mcpi.block as block
from mcpi.block import Block
from mcpi.vec3 import Vec3

# castle ground floor plan
#   sss                        sss   5
#  s   s                      s   s  4
# s     s                    s     s 3
# s  s  ssssgsssgsssgsssgsssss  s  s 2
# s   ww www www www www www www   s 1
#  s  w                        w  s  03
#   ssw                        wss    9
#    sw                        ws    8
#    swff     c c c c c      ffws    7
#    swff    ttttttttttt     ffws    6
#    swff   ctttttttttttc    ffws    5
#    swff    ttttttttttt     ffws    4
#    sw       c c c c c        ws    3
#    sw                        ws    2
#    sw                        ws    1
#    swwwwdwwwddwwwwwwddwwwwwwwws    02
#    sssss sss  ssssss  sssssssss    9
#    d          xxwwxx          d    8
#    sssss ss   xxwwxx   ssssssss    7
#    s      s     xx     sbbbbb s    6
#    s      s     xx     sb     s    5 
#    s            xx     sb     s    4
#    s            xx     sb     s    3
#    s      s                   s    2
#    s      s                   s    1
#    ssss  ss   p    p   ss  ssss    01
#    s      s            s      s    9
#    s      s            s      s    8
#    s                          s    7
#   ss                          ss   6
#  s        s            s        s  5 
# s         s    sdds    s         s 4
# s  s  ssssssssss  ssssssssss  s  s 3
# s     s                    s     s 2
#  s   s                      s   s  1
#   sss                        sss   0
# 
# 3210987654321098765432109876543210
#    3         2         1          

# initial 2nd floor plan:
#   sssssssgsssgsssgsssgssssssss 9
#   s  w                    w  s 8
#   s  w                    w  s 7
#   s  w                    w  s 6
#   s  w                    w  s 5
#   s  w                    w  s 4
#   s  w                    w  s 3
#   s  w                    w  s 2
#   s  w                    w  s 1
#   s  wwwwwwwwwwddwwwwwwwwww  s 02
#   s                          s 9
#   s                          s 8
#   swwwwwww            wwwwwwws 7
#   s      w   ffffff   w      s 6
#   d      w   xxwwxx   w      d 5
#   s      w   xxwwxx   w      s 4
#   s storew  f      f  w brew s 3
#   s      d  f      f  d      s 2 
#   s      d  f      f  d      s 1
#   swwwwwww  ffffffff  wwwwwwws 01
#   s      d            d      s 9
#   s      d            d      s 8
#   s      w  wwwddwww  w      s 7
#   s smeltw  w      w  w dye  s 6
#   s      w  w      w  w      s 5
#   s      w  w craftw  w      s 4
#   swwwwwww  w      w  wwwwwwws 3
#   s         w      w         s 2 
#   s         w      w         s 1
#   ssssssssssssssssssssssssssss 0

#   7654321098765432109876543210
#          2         1          
class Castle(BuildingEx):
	# * all levels 4 spaces high (need 5 for smelting room)
	#      Mine entrance room somewhere, stairs to base ment under main stairs
	#
	#
	# oak wood rafters on ceilings & columns in atrium at start of stairs
	# for realism extend into walls, will need to add butresses on outer walls to shield beam ends
	# need to plan beam & column placement on all floors including basement & upper floor,
	# and then figure out butresses on outer wall
	# 
	#		draft build order:
	#		floor (stone bricks) 2 layers
	#		castle walls 
	#		ground floor rooms
	#		corner turrets - 3x3 interior square surrounded with walls 3m long, no coner blocks (for a 5x5 "circle")
	#			- start turrets from seconds floor tapering in to wall on ground floor
	#		any remaining walls, windows & doors
	#		2nd floor floor
	#		main stairs & balcony
	#		2nd floor rooms
	#		corner turrets
	#		any remaining walls & windows
	#		balconys & doors
	#		rafters & support beams
	#		roof
	#		basement, stairs, corridor, mushroom farm, target practice, portal, mine access & mob farm access
	# Think about mob jail for curing villager to add to village
	# 
	# Probably going to need soul sand & nether wart farm for brewing potions
	#
	WALLS_CORNER_POS = {'South East' : Building.SE_CORNER_POS + Vec3(-3,0,-3), 
						'South West' : Building.SE_CORNER_POS + Vec3(-30,0,-3),
						'North West' : Building.SE_CORNER_POS + Vec3(-30,0,-32),
						'North East' : Building.SE_CORNER_POS + Vec3(-3,0,-32) }

	WIDTH = 28
	def __init__(self, *args, **kwargs):
		super(Castle, self).__init__(width=Castle.WIDTH, *args, **kwargs)
						
	def _create_surrounding_walls(self, level):
		builds = []
		# build surrounding walls
		builds.append(BuildingBlock(Castle.WALLS_CORNER_POS['South East'] + Vec3(0,level,0),
									EXTERIOR_WALLS,
									Castle.WALLS_CORNER_POS['South West'] + Vec3(0,WALL_HEIGHT + level,0),
									description="South wall"))
		builds.append(BuildingBlock(Castle.WALLS_CORNER_POS['South West'] + Vec3(0,level,0),
									EXTERIOR_WALLS,
									Castle.WALLS_CORNER_POS['North West'] + Vec3(0,WALL_HEIGHT + level,0),
									description="West wall"))
		builds.append(BuildingBlock(Castle.WALLS_CORNER_POS['South East'] + Vec3(0,level,0),
									EXTERIOR_WALLS,
									Castle.WALLS_CORNER_POS['North East'] + Vec3(0,WALL_HEIGHT + level,0),
									description="East wall"))
		builds.append(BuildingBlock(Castle.WALLS_CORNER_POS['North East'] + Vec3(0,level,0),
									EXTERIOR_WALLS,
									Castle.WALLS_CORNER_POS['North West'] + Vec3(0,WALL_HEIGHT + level,0),
									description="North wall"))
		self._add_section("Ground floor enclosing walls", builds)


	def _create_ground_floor_skeleton(self):
		builds = []
		builds.append(SubBuilding(GroundFloor(Building.NORTH), Castle.WALLS_CORNER_POS['South East']))
		self._add_section("Floor", builds)

		self._create_surrounding_walls(0)

		# Side doors
		builds.append(Door(Door.HINGE_LEFT, 
							Castle.WALLS_CORNER_POS['South East'] + Vec3(0,0,-15),
							block.DOOR_WOOD.withData(Door.EAST),
							description="East side door"))
		builds.append(Door(Door.HINGE_RIGHT, 
							Castle.WALLS_CORNER_POS['South West'] + Vec3(0,0,-15),
							block.DOOR_WOOD.withData(Door.WEST),
							description="West side door"))

		# Front wall & door
		builds.append(Door(Door.HINGE_RIGHT, 
							Castle.WALLS_CORNER_POS['South East'] + Vec3(-13,0,0),
							block.DOOR_WOOD.withData(Door.SOUTH),
							description="Front door"))
		builds.append(Door(Door.HINGE_LEFT, 
							Castle.WALLS_CORNER_POS['South East'] + Vec3(-14,0,0),
							block.DOOR_WOOD.withData(Door.SOUTH),
							description="Front door"))
		self._add_section("Ground floor external doors", builds)

		
	def _create_ground_floor_rooms(self):
		builds = []
		builds.append(SubBuilding(DiningHall(Building.NORTH), 
								  Castle.WALLS_CORNER_POS['South East'] + Vec3(0,0,-16)))

		builds.append(SubBuilding(Kitchen(Building.WEST), 
								  Castle.WALLS_CORNER_POS['South East'] + Vec3(-20,0,-14)))
		builds.append(SubBuilding(Pantry(Building.WEST), 
								  Castle.WALLS_CORNER_POS['South East'] + Vec3(-20,0,-7)))

		builds.append(SubBuilding(EnchantingRoom(Building.EAST), 
								  Castle.WALLS_CORNER_POS['South East'] + Vec3(-7,0,-7)))
		builds.append(SubBuilding(Smithy(Building.EAST), 
								  Castle.WALLS_CORNER_POS['South East'] + Vec3(-7,0,0)))


		self._add_section("Ground floor rooms", builds)

	def _create_upper_floor_and_main_staircase(self):
		builds = []
		# after applying 2nd storey floor, add main stairs
		builds.append(SubBuilding(UpperFloor(Building.NORTH), 
								  Castle.WALLS_CORNER_POS['South East'] + Vec3(0,WALL_HEIGHT + 1,0)))
		builds.append(SubBuilding(MainStairs(Building.NORTH), 
								  Castle.WALLS_CORNER_POS['South East'] + Vec3(-11,0,-10)))
		self._add_section("Upper floor & staircase", builds)

	def _create_ground_floor_fittings(self):
		# TODO: add class for main doorway
		# add windows & torches & turret bases
		pass

	# Ground floor:
	#	   main stairs
	#      dining hall at back,
	#      kitchen & pantry on one side
	#      smithy & enchanting room on other side.
	#      hallway to back/side door on smithy side
	def _create_ground_floor(self):
		self._create_ground_floor_skeleton()
		self._create_ground_floor_rooms()
		self._create_upper_floor_and_main_staircase()
		self._create_ground_floor_fittings()

	def _create_second_floor_skeleton(self):
		self._create_surrounding_walls(6)
		# TODO: add windows & torches & turrets
				
	def _create_second_floor_rooms(self):
		builds = []
		builds.append(SubBuilding(StoreRoom(Building.WEST), 
								  Castle.WALLS_CORNER_POS['South East'] + Vec3(-20,0,-17)))
		builds.append(SubBuilding(SmeltingRoom(Building.WEST), 
								  Castle.WALLS_CORNER_POS['South East'] + Vec3(-20,0,-10)))

		builds.append(SubBuilding(DyeRoom(Building.EAST), 
								  Castle.WALLS_CORNER_POS['South East'] + Vec3(-7,0,-3)))
		builds.append(SubBuilding(Brewery(Building.EAST), 
								  Castle.WALLS_CORNER_POS['South East'] + Vec3(-7,0,-10)))

		builds.append(SubBuilding(CraftingRoom(Building.SOUTH), 
								  Castle.WALLS_CORNER_POS['South East'] + Vec3(-17,0,-7)))

		builds.append(SubBuilding(Bedroom(Building.NORTH), 
								  Castle.WALLS_CORNER_POS['South East'] + Vec3(-3,0,-20)))

		self._add_section("Second storey room shells", builds)

	# first story
	# - master bedroom
	#      - Penthouse on roof to overlook walls.
	#      - 2 beds surrounded by fence posts with pressure plates & carpet on top for 4 poster
	#      - chest at end of bed
	#           => 4x4 area for bed + 2 minimum all round
	#      - fireplace
	# - store room (non food)
	#      - Sell-able stuff (near door, beside armory)
	#           - wheat, potato, carrots
	#           - string, coal, wool, 
	#           - paper, books
	#           - rotten meat
	#           - raw pork, raw chicken
	#           - leather.
	#      - building material
	# - crafting room, close to store
	# - smelting room -  will need to be 5 high
	# - brewery
	# - dye room
	def _create_second_floor(self):
		self._create_second_floor_skeleton()
		self._create_second_floor_rooms()

	# TODO: create roof from uppper floor class.
	# add another level on turrets with access to roof
	# add turret tops with battlements
	# add surrounding battlements on roof (overhang & fences?)
	def _create_roof(self):
		builds = []
		builds.append(SubBuilding(UpperFloor(Building.NORTH), 
								  Castle.WALLS_CORNER_POS['South East'] + Vec3(0,(WALL_HEIGHT*2) + 3,0)))

	# TODO: create stairs to basement
	# basement
	#	target practice room
	#	corridor
	#	mushroom farm
	#	portal room
	#	mine access
	#	mobtrap access
	def _create_basement(self):
		pass

	def _create_structure(self):
		super(Castle, self)._create_structure()
		self._create_ground_floor()
		self._create_second_floor()
		self._create_roof()
		self._create_basement()



class CastleEnclosure(BuildingEx):
	 #* well(s)

	 #* crop farm x4 - 2 wheat, 1 potato 1 carrot
	 #     - make plot sizes 8x7, with 7x dispensers - will need to work on surrounding automation for this.
	 #          - but could put the dispensers on the bottom easing automation
	 #          - could use redstone torches underneath dispensers & lever with power on normally
	 #     - this will run to 8x19 x 2
	 #* sugar cane farm x2 (10x9 for 1 plot)
	 #* pumpkin/melon farm - need to investigate designs.
	 #     http://minecraft.gamepedia.com/Tutorials/Pumpkin_and_melon_farming
	 #     check out semi automatic stackable design #7
	 #* mushroom farm - can go under other farms. (20x25 working well - although some mobs spawn inside)

	 #* Animal pens (make fences 2 high with double gates in 1 corner (animals are escaping from stiles in current designs)
	 #     - pens sizes (current = 9x8, maybe go to 10x10)
	 #     - cows, sheep, pigs, chickens
	 #     - could use leads to keep animals in pens.
	 #     - probably want a paddock area for horses too (horses can walk through non solid blocks so maybe just a stables)
	 #* stables - need to work on designs
	 #     - individual stalls & hay inside?
	 #     https://www.pinterest.com/mustanglani/minecraft-barns/
	 #     https://www.google.ie/search?q=minecraft+stable+blueprint&sa=X&biw=1920&bih=958&tbm=isch&tbo=u&source=univ&ei=M9g0Vd3UIoLW7AbXsYHQDA&ved=0CCAQsAQ
	 #     http://www.minecraftforum.net/forums/show-your-creation/screenshots/1588012-howto-build-a-barn (17x17 design, might no need such a high roof (try half slab steps for roof)
	 #* kennels - need to work on designs.
	 #     - think i read a dog bed design - 2 half slabs, with carpet on top & surrounded by signs.
	 #     http://mp3loot.ninja/index.php?q=20+wolf+dog+house+kennel+ideas+and+designs+minecraft&type=video&view=696d525161544e53795838

	 #* pond?

	pass
