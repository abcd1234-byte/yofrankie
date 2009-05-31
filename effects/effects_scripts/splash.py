# this script is applied to one empty,
# using multiple collision sensors on water surfaces to detect the splash
# the empty will be moved to the collision location and instantly add the object
# this needs to be done because groups cant be moved once added by addObject actuators.

def main(cont):
	own_add_empty = cont.owner
	
	addob_actu = cont.actuators['splash_create']
	
	for sens in cont.sensors: # one or more water surface meshes	
		ob_water = sens.owner
		
		if not sens.positive:
			continue
		
		last_ob = addob_actu.objectLastCreated
		
		if last_ob:	last_pos = last_ob.worldPosition
		else:		last_pos = None
		
		for ob in sens.hitObjectList:
			pos = ob.worldPosition
			
			if last_pos:
				dist = abs(pos[0]-last_pos[0]) + abs(pos[1]-last_pos[1])
				if dist < 0.5:
					continue
			
			#if liquid plane is water, not lava, consider size of object impacting it to add splash, or splash_small
			if ob_water.has_key('water'):
				if ob.has_key('pickup'):
					addob_actu.object = "fx_splash_small"
				else:
					addob_actu.object = "fx_splash"
			
			own_add_empty.localPosition = pos
			
			# We want to add multiple so this wont do
			# GameLogic.addActiveActuator(addob_actu,1)
			addob_actu.instantAddObject()
