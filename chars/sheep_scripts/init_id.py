import GameLogic

def main(cont):
	# Give the sheep a unique ID
	try:
		ID = GameLogic.ID = GameLogic.ID + 1
	except:
		ID = GameLogic.ID = 0
	
	own = cont.owner
	# For respawning.
	own['x_orig'], own['y_orig'], own['z_orig'] = own.worldPosition
	own['id'] = ID
	# print "setting ID", ID


	# Warning!!! This only works when inside dupliGroups
	#   since objects in hidden layers will still show up as a sensor.

	# Assign dummy value
	own['own_rig'] = 0
	for ob in own.children:
		name = ob.name[2:]
		
		if 'rig_ram' in name:
			own['type'] = 'ram'
			del own['carried'], own['projectile'], own['kickable']
			break
		elif 'rig_sheep' in name:
			own['type'] = 'shp'
			break
		elif 'rig_rat' in name:
			own['type'] = 'rat'
			#del own.carried
			break
		
		# Theres an an odd bug with flawsh_death object adder
		# set the object by name and it should help
		# This should not be needed
		'''
		actu = cont.actuators['create_poof']
		actu.object = 'flash_death'
		'''
	
	cont.activate('default_state')
