# This sucks a bit, it updates both players life meters rather then just 1

import Rasterizer
import GameLogic

def main(cont):
	own= cont.getOwner()
	
	# We are not sure the player has initialized
	try:
		PLAYER_COUNT = GameLogic.globalDict['CONFIG']['PLAYER_COUNT']
	except:
		print "\twarning hud: this should be run as an overlay to frankie\n\tkeep going for testing purposes"
		PLAYER_COUNT = 2
	
	# Dont show the p2 hud if we are playing single player
	
	if PLAYER_COUNT == 1:
		GameLogic.addActiveActuator( cont.getActuator("end_p2"), True )
	
	for actu in cont.getActuators():
		actu_own = actu.getOwner()
		if actu_own.getName().startswith('OBitem_'):
			actu_own.setVisible(False, True) # recursive, sets text invisible also
	
	'''
	print dir(own)
	# set crap in a 
	point_p1 = [0.0,0.0,0.0]
	
	while own.pointInsideFrustum(point_p1):
		point_p1[2] += 0.02
	
	point_p1[2] -= 0.02
	
	while own.pointInsideFrustum(point_p1):
		point_p1[0] += 0.02
	
	point_p1[0] -= 0.02
	
		
	# own.perspective = 0
	cont.getActuator("end_p2").getOwner().setPosition(point_p1)
	
	Rasterizer.setMaterialMode(0)
	
	'''
	
	GameLogic.addActiveActuator( cont.getActuator("hud_monitor_state"), True )
