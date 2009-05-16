# mostly copied from action_all.py, do_throw_carry() , since dropping and throwing are similar

'''
run this script if we die or drown while carrying
'''

def main(cont):
	'''
	Throw items your carrying ontop of your head
	'''
	own = cont.getOwner()
	
	ob_parent = cont.getSensor('carry_pos_linkonly').getOwner()
	
	try:
		own_carry = ob_parent.getChildren()[0]
	except:
		# was nothing to carry
		own.carrying = 0
		return
	
	own_carry.removeParent()
	own.carrying = 0
	own_carry.carried = 0
	
	# Tell the object we threw it. so we cant hurt ourselves
	if hasattr(own_carry, 'projectile_id'):
		own_carry.projectile_id = own.id
	
	own_y = own.getAxisVect([0,2,0])
	own_y[2] = 0.0
	own_carry.setLinearVelocity([own_y[0],own_y[1], 3], 0) # We are carrying sideways
	
	# Notes 
	# * set upright while in the falling with interpolation or landing.
	# * dont need to turn the carry animation off, its done via a property check.

	