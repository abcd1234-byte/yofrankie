# This sucks a bit, it updates both players life meters rather then just 1

import Rasterizer
import GameLogic

def main(cont):
	own= cont.owner
	
	# We are not sure the player has initialized
	try:
		PLAYER_COUNT = GameLogic.globalDict['CONFIG']['PLAYER_COUNT']
	except:
		print "\twarning hud: this should be run as an overlay to frankie\n\tkeep going for testing purposes"
		PLAYER_COUNT = 2
	
	# Dont show the p2 hud if we are playing single player
	
	if PLAYER_COUNT == 1:
		cont.activate("end_p2")
	
	for actu in cont.actuators:
		actu_own = actu.owner
		if actu_own.name.startswith('OBitem_'):
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
	cont.actuators["end_p2"].owner.localPosition = point_p1
	
	Rasterizer.setMaterialMode(0)
	
	'''
	cont.activate("hud_monitor_state")

