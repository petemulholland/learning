from base.utils import *
from base.rooms import *
from base.castle import Castle
from base.debug.debug_base import mc, pl, debug_building
from utils import setup_test_area

if __name__ == "__main__":
	#search_result = search_chunk_for(DOOR_WOOD, 0, 0, search_at, abortive_block_ids)
	# TODO: debug fireplace builds, coords don't look right
	#global mc
	#setup_test_area(mc)
	
	#debug_dining_hall()
	#debug_building(Kitchen)
	#debug_building(Pantry)
	#debug_building(EnchantingRoom)
	#debug_building(Smithy)
	#debug_building(DiningHall)
	#debug_building(MainStairs)
	debug_building(Castle)



