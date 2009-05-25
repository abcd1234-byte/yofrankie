# this script is applied to one empty,
# using multiple collision sensors on water surfaces to detect the splash
# the empty will be moved to the collision location and instantly add the object
# this needs to be done because groups cant be moved once added by addObject actuators.

def main(cont):
	own_add_empty = cont.getOwner()
	
	addob_actu = cont.getActuator('splash_create')
	
	for sens in cont.getSensors(): # one or more water surface meshes	
		
		ob_water = sens.getOwner()
		if not sens.isPositive():
			continue	
		
		last_ob = addob_actu.getLastCreatedObject()
		
		if last_ob:	last_pos = last_ob.getPosition()
		else:		last_pos = None
		
		for ob in sens.getHitObjectList():
			pos = ob.getPosition()
			
			if last_pos:
				dist = abs(pos[0]-last_pos[0]) + abs(pos[1]-last_pos[1])
				if dist < 0.5:
					continue
			
			#if liquid plane is water, not lava, consider size of object impacting it to add splash, or splash_small
			if hasattr(ob_water, "water"):
				if hasattr(ob, "pickup"):
					addob_actu.setObject("fx_splash_small")
				else:
					addob_actu.setObject("fx_splash")
			
			own_add_empty.setPosition(pos)
			
			# We want to add multiple so this wont do
			# GameLogic.addActiveActuator(addob_actu,1)
			addob_actu.instantAddObject()
