# import frank_ledge_module
import GameLogic
from Mathutils import CrossVecs, Vector, Matrix, RotationMatrix, AngleBetweenVecs
from ledge_test import frankTestLedge, CLIMB_HANG_Y_OFFSET, CLIMB_HANG_Z_OFFSET

def do_reset_timeofs(cont):
	own_rig = cont.getSensor('rig_linkonly').getOwner() # The rig owns this! - cheating way ti get the rig/
	own_rig.timeOffset = own_rig.defTimeOffset


def do_fall_state(own, cont):
	GameLogic.addActiveActuator(cont.getActuator('fall_state'), True)
	own.setLinearVelocity([0,0,2])
	own.ledge_regrip_timer = 0.0
	do_reset_timeofs(cont)


def main(cont):
	
	HANG_COUNTER_GRAVITY = 0.17
	# HANG_TIMEOFFSET = 20.0
	
	own = cont.getOwner()
		
	# 3rd arg gets a corrected ray when its thr first ray for the state
	# This can only run the first time otherwise it makes shimmy jitter baddly.
	#	since correcting the axis can rotate frankie back and fourth.
	if cont.getSensor('true_init_pulse_ledge').isPositive():
		ledge_hit, ledge_nor, zpos = frankTestLedge(own, cont, None, False)
	else:
		
		# Drop on purpose
		sens_keyDown = cont.getSensor('key_down')
		if sens_keyDown.isPositive() and sens_keyDown.isTriggered():
			do_fall_state(own, cont)
			return
		
		
		ledge_hit, ledge_nor, zpos = frankTestLedge(own, cont, None, True)
		
		# set the timeoffset so hanging gets nice smooth movement for free.
		# cont.getSensor('rig_linkonly').getOwner().timeOffset = HANG_TIMEOFFSET
	
	if not ledge_hit:
		do_fall_state(own, cont)
		return
	
	sens_up = cont.getSensor('key_up')
	if sens_up.isPositive() and sens_up.isTriggered() and own.can_climb:
		# own.suspendDynamics()
		do_reset_timeofs(cont)
		GameLogic.addActiveActuator(cont.getActuator('climb_state'), True)
		return
	
	own.setLinearVelocity([0,0, HANG_COUNTER_GRAVITY])
	
	# Make sure frankie is upright. especially if he was just gliding this can happen!
	own.alignAxisToVect([0,0,1], 2)
	
	# We need to do somthing a bit extra tricky here, move the position of frankie around the ray intersect pivot,
	# This avoids jittering
	new_dir = Vector(-ledge_nor[0], -ledge_nor[1], 0.0)
	new_z = zpos + CLIMB_HANG_Z_OFFSET
	own_y = Vector( own.getAxisVect([0,1,0]) )
	ledge_hit = Vector(ledge_hit)
	cross =CrossVecs(own_y, new_dir)
	ang = AngleBetweenVecs(own_y, new_dir)
	
	# Set Frankies distance from the hit position
	
	if ang > 0.1:
		if cross.z < 0:
			ang = -ang
		
		pos_orig = Vector(own.getPosition())
		####pos_new = ((pos_orig-ledge_hit) * rot) + ledge_hit
		# Do this instead.

		d = (pos_orig-ledge_hit)
		d.z = 0.0
		d.length = -CLIMB_HANG_Y_OFFSET

		pos_new = (d*RotationMatrix(ang, 3, 'z')) + ledge_hit
		
	else:
		# Simple but not good enough
		# own.setPosition( (pos_orig-ledge_hit) + ledge_hit )

		# Location, use CLIMB_HANG_Y_OFFSET to offset ourselves from the ledges hit point
		d = Vector(ledge_nor)
		d.z = 0.0
		d.length = -CLIMB_HANG_Y_OFFSET
		pos_new = d + ledge_hit
	
	own.alignAxisToVect([-ledge_nor[0], -ledge_nor[1], 0.0], 1)
	pos_new.z = new_z
	own.setPosition(pos_new)
	
