'''
When frankie is airboure he can double jump and glide
This script checks for conditions where this is ok and changes the state.

It also clamps the fall speed and detects when he is going to land so it can play the animation
'''
import GameLogic

from Mathutils import Vector

DBL_JUMP_KEYHELD = 0
DBL_JUMP_OK = 1
DBL_JUMP_DONE = 2
DBL_JUMP_MISSED = 3
DBL_JUMP_DELAY = 4 # Delayed jumping means double jump wes pressed really fast and we have to delay before applying


DBL_JUMP_FALL_MARGIN = -1.4 # how fast you can be falling before you cant double jump anymore
DBL_JUMP_BEGIN_TIME = 0.3 # How long after jumping your allowed to double jump
	

def do_pradict_land(own, cont, velocity):
	# Check if we should land?
	if velocity[2] < -2.0: # Check downward falling velocity, 0.0 could be used but -2.0 seems good enough
		ray_to = own.getPosition()
		ray_to[2] -= 10.0
		if own.rayCastTo(ray_to, 0.6, 'ground'):
			GameLogic.addActiveActuator(cont.getActuator('landing'), True)
			GameLogic.addActiveActuator(cont.getActuator('landing_snd'), True)


def do_clamp_speed(own, cont, velocity):		
	'''
	Clamp the x/y velocity, we can do speedups etc here
	but for now just clamping at around run speed is fine.
	'''
	velocity_vec = Vector(velocity[0], velocity[1])
	l = velocity_vec.length


	if own.boosted:
		MAX_SPEED = 3.0	
	else:
		MAX_SPEED = 6.0	
	
	if l < MAX_SPEED:
		return
	
	velocity_vec.length = MAX_SPEED
	
	velocity[0] = velocity_vec[0]
	velocity[1] = velocity_vec[1]
	
	own.setLinearVelocity(velocity)

def do_double_jump(own, cont, dropping_dir, actu_dbl_jump_anim, actu_dbl_jump_force):
	if dropping_dir > DBL_JUMP_FALL_MARGIN: # 0.2 to allow SOME falling
		if own.jump_time < DBL_JUMP_BEGIN_TIME:
			own.double_jump = DBL_JUMP_DELAY
		else:
			# Do the double jump
			# print "Reset Actuator 2", actu_dbl_jump_anim.getStart()
			# actu_dbl_jump_anim.setFrame( actu_dbl_jump_anim.getStart() )
			
			GameLogic.addActiveActuator(actu_dbl_jump_anim, True)
			actu_dbl_jump_anim = None
			
			GameLogic.addActiveActuator(actu_dbl_jump_force, True)
			actu_dbl_jump_force = None # Dont disable this
			
			own.double_jump = DBL_JUMP_DONE
			own.jump_time = 100.0 # So we know how long we have jumped for before gliding
			return True
	else:
		# We are falling so set the double jump done so we can glide.
		own.double_jump = DBL_JUMP_MISSED
		return False
	# Even if we  didnt double jump, tag as done. this way glide works
	return False


def do_glide_state(own, cont, velocity):
	# We know this cant be done before double jumping or missing a double jump
	# print cont.getSensor('any_collide').isPositive(), cont.getSensor('any_collide').getHitObjectList(), 
	###print [o.name for o in cont.getSensor('any_collide').getHitObjectList()]
	
	if velocity[2] > 0.0: # we must be falling
		return
	
	if cont.getSensor('collide_any').isPositive():
		return
	
	# print dir(cont.getSensor('any_collide'))
	if	own.double_jump == DBL_JUMP_MISSED  or  \
		(own.double_jump == DBL_JUMP_DONE  and  own.jump_time > 100.3): # and \
		# Note, own.jump_time over 100.0 will give a limit so you cant double jump right away
		
		
		# Other logic that didnt work so well
		# (not cont.getSensor('any_collide').isPositive()):
		# (own.double_jump == DBL_JUMP_DONE and (actu_dbl_jump_anim.getFrame() > actu_dbl_jump_anim.getEnd()-1.0)):
		
		GameLogic.addActiveActuator(cont.getActuator('glide_state'), True)

def main(cont):
	
	own = cont.getOwner()
	
	# own.restoreDynamics() # WE SHOULDNT HAVE TO CALL THIS HERE
	
	
	# print [o.name for o in cont.getSensor('any_collide').getHitObjectList()]
	
	velocity = own.getLinearVelocity()
	
	
	# Done by an actuator now. we could add this back and remove the actuator.
	# but nicer to use user visible logic bricks.
	# own.alignAxisToVect([0,0,1], 2, 0.1)
	
	do_clamp_speed(own, cont, velocity)
	do_pradict_land(own, cont, velocity)
	
	KEY_JUMP = cont.getSensor('key_jump').isPositive()
	
	
	
	actu_dbl_jump_anim = cont.getActuator('doublejump')
	actu_dbl_jump_force = cont.getActuator('double_jump_force')	
	double_jump_done = False
	
	# Did we just enter this state?
	if cont.getSensor('generic_true_pulse').isPositive():
		if own.jump_time < 0.3:
			if not KEY_JUMP: # This is very unlikely since we only JUST sstarted jumping. in cases where we fall off a ledge its possible still.
				own.double_jump = DBL_JUMP_OK # Key is released, we can double jump next time its pressed.
			else:
				own.double_jump = DBL_JUMP_KEYHELD # We are not sure they were jumping so be sure to check the timer.
	else:		
		# Not bouncing
		if KEY_JUMP or own.double_jump == DBL_JUMP_DELAY:
			
			# Cant double jump or glide while carrying.
			if not own.carrying:
				
				if own.double_jump == DBL_JUMP_OK or own.double_jump == DBL_JUMP_DELAY:
					double_jump_done =  do_double_jump(own, cont, velocity[2], actu_dbl_jump_anim, actu_dbl_jump_force)
				else:
					do_glide_state(own, cont, velocity)
		else:
			if own.double_jump == DBL_JUMP_KEYHELD:
				own.double_jump = DBL_JUMP_OK # Key is released, we can double jump next time its pressed.
	
	# If actions are not None, assume we didint want to suse them
	
	if not double_jump_done:
		GameLogic.addActiveActuator(actu_dbl_jump_force, False)	
	
	# Add falling animations
	# print '%.4f' % velocity[2]
	# Use the right falling animation, falling up or down?
	if velocity[2] > 0.0:
		GameLogic.addActiveActuator(cont.getActuator('fall_down'), False)
		GameLogic.addActiveActuator(cont.getActuator('fall_up'), True)
	else:
		GameLogic.addActiveActuator(cont.getActuator('fall_up'), False)
		GameLogic.addActiveActuator(cont.getActuator('fall_down'), True)
