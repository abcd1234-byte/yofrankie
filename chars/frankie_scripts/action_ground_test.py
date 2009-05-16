'''
its a pitty we need this script at all, but knowing if we are on the ground or not isnt that simple
basically use ray and collision sensors to detect of we are on the ground, keeping the "grounded" property up to date
there may be a better way to do this, like use second collision object at frankies feet- but for now this is OK.
'''
import GameLogic

def main(cont):
	own = cont.getOwner()
	# print dir(cont)
	
	# Cant land while being carried
	if own.carried:
		return
	
	#FALL_LIMIT = -0.5 # How much we need to be falling before the ray cast is used
	
	sens_touchGround = cont.getSensor('ground_test')
	# sens_ledgeCollide = cont.getSensor('ledge_collide')
	
	
	# Note, cont.getSensor('ground_ray') sensor isnt strictly needed however adding this avoids jitter when running over bumps.
	if sens_touchGround.isPositive() or (cont.getSensor('ground_ray').isPositive() and own.jump_time > 0.5):
		if own.grounded == 0: # was flying
			# print own.getLinearVelocity()[2], 'own.getLinearVelocity()[2]'
			# print own.jump_time, 'own.jump_time' 
			
			# Change the state
			act_state = cont.getActuator('idle_state')
			GameLogic.addActiveActuator(act_state, True)
			own.grounded = 1
			
			# print " SETTING ON GROUND "
	else: # off the ground
		if own.grounded == 1: # just left the ground
			# Change the state
			act_state = cont.getActuator('fall_state')
			GameLogic.addActiveActuator(act_state, True)
			own.grounded = 0
			# print " SETTING ON AIR "
