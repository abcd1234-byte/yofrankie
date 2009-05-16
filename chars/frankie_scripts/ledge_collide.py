'''
Run when frankie is falling or gliding

when frankies ray intersects with a ledge, run this script.
If he can grab it, move to the grab state.

Most of the logic here is in "ledge_test.frankTestLedge"
'''
import GameLogic
import Mathutils
from ledge_test import frankTestLedge

def main(cont):
	REGRIP_TIME = 0.8 # How long before you regrip
	HANG_TIMEOFFSET = 20.0

	own = cont.getOwner()
	
	if own.ledge_regrip_timer < REGRIP_TIME or own.carried or own.carrying:
		return
	
	sens_ledge = cont.getSensor('ledge_collide')
	if not sens_ledge.isPositive():
		return
	
	# print "LEDGE TOUCHING", sens_ledge.isPositive()
	
	if frankTestLedge(own, cont, sens_ledge.getHitObject(), False)[0] != None:
		
		# We have collided with an edge, pressing up again will climb the edge
		own.setLinearVelocity([0.0, 0.0, 0.0])
		
		# set the timeoffset so hanging gets nice smooth movement for free.
		
		# Make sure frankie is upright. especially if he was just gliding this can happen!
		own.alignAxisToVect([0,0,1], 2)
		
		cont.getSensor('rig_linkonly').getOwner().timeOffset = HANG_TIMEOFFSET
		GameLogic.addActiveActuator(cont.getActuator('hang_state'), True)
		return
	
	#print "Missed"
	print '\tledge_grab: could not grab ledge'
