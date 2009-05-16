'''
When falling and colliding with an object with the "bounce"
property, you will bounce back up. If youre pressing jump youll bounce higher.
'''
import GameLogic

def main(cont):
	# BOUNCE_FALL_SPEED = 0.0
	BOUNCE_Z_DIST = 0.2 # How much higher you must be then what you are jumping on.
	
	own = cont.getOwner()
	
	actu_dbl_bounce_force = cont.getActuator('bounce_force')	
	
	if not cont.getSensor('bounce_hit').isPositive(): #  and own.getLinearVelocity()[2] < BOUNCE_FALL_SPEED:
		GameLogic.addActiveActuator(actu_dbl_bounce_force, False )
		return
	
	hit_ob = cont.getSensor('bounce_hit').getHitObject()		
	
	own_z = own.getPosition()[2]
	hit_z = hit_ob.getPosition()[2]
	
	if own_z - hit_z < BOUNCE_Z_DIST:
		print '\tbounce: must be above object to bounce on it'
		return
	
	# Tell the object it has been bounced on!
	# It must do its own logic to react
	if hasattr(hit_ob, 'bounce'):
		hit_ob.bounce = 1 
	
	KEY_JUMP = cont.getSensor('key_jump').isPositive()
	
	# Are we touching a bouncy object?
	if KEY_JUMP:
		actu_dbl_bounce_force.setLinearVelocity(0,0,6,1)
		own.double_jump = 0 # DBL_JUMP_KEYHELD
	else:
		actu_dbl_bounce_force.setLinearVelocity(0,0,4,1)
		own.double_jump = 1 # DBL_JUMP_OK
	
	GameLogic.addActiveActuator(actu_dbl_bounce_force, True)
	GameLogic.addActiveActuator( cont.getActuator('jumping'), True )
	GameLogic.addActiveActuator( cont.getActuator('sfx_bounce'), True )
	
	# print '\tFrankBouncing!'	
