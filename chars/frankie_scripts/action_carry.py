'''
Run when a carry object hits us and attach it to our hand if all is right (and the moons are aligned)
'''
import GameLogic
from  Mathutils import Matrix

# We use this a lot, just to be neat
def dontCatch(cont):
	GameLogic.addActiveActuator( cont.getActuator('catch'), False )	


def do_catch(cont, own, ob_carry, ob_catch_bonechild):
	
	own_pos = own.getPosition()
		
	'''
	If we are ok to catch an object, this function runs on all catchable objects
	and catches the first catchable one since its possible we collide with multiple.
	'''
	
	if hasattr(ob_carry, 'grounded') and ob_carry.grounded != 0:
		print '\tcant catch: carry object not airbourne'
		return False
	
	if ob_carry.carried == 1:
		print '\tcant catch: alredy being carried by another'
		return False
	
	ob_carry_pos = ob_carry.getPosition()
	
	if ob_carry_pos[2] < own_pos[2]+0.1:
		print '\tcant catch: catch objects Z position too low'
		return False
	
	# is it falling down?
	# - Note, dont do this. once its hit your head its velovcity changes so we cant rely on it
	'''
	if ob_carry.getLinearVelocity()[2] > 0.0:
		print "\tcarry? not falling"
		return False
	'''
	# Is it close enough to the center?
	# - Note, dont do this. if it touches we can carry, otherwise stuff sits on your head and nothing happens.
	'''
	if abs(ob_carry_pos[1] - pos_ray_sens[1]) + abs(ob_carry_pos[0] - pos_ray_sens[0]) > 0.5:
		return False
	'''
	
	# Cannot carry a dead animal
	if hasattr(ob_carry, 'life') and ob_carry.life <= 0:
		print "\tcant catch: cant carry dead"
		return False
	
	
	
	
	# Ok, Checks are done, now execute the catch
	
	# Orient the carry objects Z axis to the -Z of the sheep,
	# since it should be upside down
	if hasattr(ob_carry, 'type') and ob_carry.type == 'shp':
		ob_catch_bonechild.alignAxisToVect(ob_carry.getAxisVect([0,0,-1]), 2)
		pos = ob_catch_bonechild.getPosition()
	else:
		# ob_catch_bonechild.alignAxisToVect(ob_carry.getAxisVect([0,1,0]), 2)
		#pos = ob_catch_bonechild.getPosition()
		#pos[2] += 1
		
		ob_catch_bonechild.alignAxisToVect(ob_carry.getAxisVect([0,0,-1]), 2)
		#ob_catch_bonechild.alignAxisToVect(ob_carry.getAxisVect([0,1,0]), 1)
		ob_carry.alignAxisToVect(own.getAxisVect([0,-1,0]), 1)
		pos = ob_catch_bonechild.getPosition()
		
		# Only for carrying frankie
		if hasattr(ob_carry, 'predator'):
			pos[2] -= 0.15
	
	
	# Set the parent
	# ob_catch_bonechild.alignAxisToVect([0,0,1], 2)
	
	ob_carry.setPosition( pos )
	# Dont touch transformation after this!
	ob_carry.setParent(ob_catch_bonechild)
	own.force_walk = -1.0
	own.carrying = 1
	ob_carry.carried = 1
	GameLogic.addActiveActuator( cont.getActuator('catch'), True)	
	GameLogic.addActiveActuator( cont.getActuator('carry_constrain_up'), True)	


def main(cont):
	own = cont.getOwner()
	
	# This object is a child of the wrist bone, it is used as the parent so the animations control the object motion
	
	
	# We are alredy carrying
	if own.carrying:
		return # Alredy carrying
	
	ob_catch_bonechild = cont.getSensor('carry_pos_linkonly').getOwner()	
	if ob_catch_bonechild.getChildren():
		print '\tcarry warning, carrying was not set but had an object in hand! - should never happen, correcting'
		own.carrying = 1
		return

	# Do some sanity checks
	if own.grounded == 0:
		print '\tcant catch anything: we are not on the ground'
		dontCatch(cont)
		return
	
	# Are we falling or doing an action?
	#	Note! use own.action_done so carrying only stops when the throwing part of the action is done.
	#	otherwise youll drop the object before throwing
	

	
	if own.action_done != 0:
		# Kicking is ok to catch
		if own.action_name=='' or own.action_name=='kick':
			pass
		else:
			print '\tcant catch anything: midst other action, not doing action', own.action_name, own.action_name
			dontCatch(cont)
			return
	
	if own.action_name != '':
		dontCatch(cont)
		return	
	
	sens_collideCarry = cont.getSensor('carry_collider')
	
	if not sens_collideCarry.isPositive():
		print '\tcant catch anything: carry collider false'
		dontCatch(cont)
		return
	
	
	# Now we know we are in a fine state to catch an object
	# look through all catch collisions and catch the first one we can.
	# its unlikely there will ever be more then 2 or 3 but this is safest.
	
	for ob_carry in sens_collideCarry.getHitObjectList():
		if do_catch(cont, own, ob_carry, ob_catch_bonechild):
			return
	
	# If we are still here it means we couldnt catch anything
	dontCatch(cont)
