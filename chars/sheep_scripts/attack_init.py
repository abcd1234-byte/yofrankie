import GameLogic

def main(cont):
	own = cont.getOwner()
	
	if own.type == 'shp':
		return
	
	sens_attack = cont.getSensor('predator_collide')
	
	predator_ob = sens_attack.getHitObject()
	
	if not predator_ob:
		return
	
	if not (hasattr( predator_ob, 'hit' ) and hasattr( predator_ob, 'hit' )):
		print '\tattack: predator missing "hit" or "life" property'
		return
	
	if predator_ob.life <= 0:
		# print '\tattack: predator alredy dead'
		return
	
	# face the predator, this is always activated
	# so we only need to spesify what to track to.
	actu_track = cont.getActuator('track_predator')
	actu_track.setObject(predator_ob)
	
	# Dont track, until we enter the state, only set the track ob
	# since the state does the tracking
	
	# Change to attacking state
	GameLogic.addActiveActuator( cont.getActuator('predator_attack_state'), 1 )
