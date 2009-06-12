'''
When falling and colliding with an object with the "bounce"
property, you will bounce back up. If youre pressing jump youll bounce higher.
'''
import GameLogic

def main(cont):
	# BOUNCE_FALL_SPEED = 0.0
	BOUNCE_Z_DIST = 0.2 # How much higher you must be then what you are jumping on.
	
	own = cont.owner
	
	actu_dbl_bounce_force = cont.actuators['bounce_force']
	
	if not cont.sensors['bounce_hit'].positive: #  and own.getLinearVelocity()[2] < BOUNCE_FALL_SPEED:
		cont.deactivate(actu_dbl_bounce_force)
		return
	
	hit_ob = cont.sensors['bounce_hit'].hitObject
	
	own_z = own.worldPosition[2]
	hit_z = hit_ob.worldPosition[2]
	
	if own_z - hit_z < BOUNCE_Z_DIST:
		print '\tbounce: must be above object to bounce on it'
		return
	
	# Tell the object it has been bounced on!
	# It must do its own logic to react
	if 'bounce' in hit_ob:
		hit_ob['bounce'] = 1 
	
	KEY_JUMP = cont.sensors['key_jump'].positive
	
	# Are we touching a bouncy object?
	if KEY_JUMP:
		actu_dbl_bounce_force.linV = (0.0, 0.0, 6.0) # global linv
		own['double_jump'] = 0 # DBL_JUMP_KEYHELD
	else:
		actu_dbl_bounce_force.linV = (0.0, 0.0, 4.0) # global linv
		own['double_jump'] = 1 # DBL_JUMP_OK
	
	cont.activate(actu_dbl_bounce_force)
	cont.activate('jumping')
	cont.activate('sfx_bounce')
	
	# print '\tFrankBouncing!'	
