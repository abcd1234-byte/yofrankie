import GameLogic

def main(cont):
	own = cont.getOwner()
	
	# be careful here, whatever is our parent should probably be told we're detaching.
	# they are not right now.
	own.removeParent()
	
	if hasattr(own, 'carried'):	
		own.carried = 0
	
	own.grounded = 0
	own.attack_type = ''
	own.life = own.lifemax
	
	if hasattr(own, 'projectile_id'):	
		own.projectile_id = -1
	
	own.target_time = 0.0
	own.revive_time = 0.0
	
	own.setLinearVelocity([0,0,0], 1)
	own.setPosition([own.x_orig, own.y_orig, own.z_orig])
	# print "respawn"
