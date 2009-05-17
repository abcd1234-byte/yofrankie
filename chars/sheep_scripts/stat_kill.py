import GameLogic

def update_hud(cont, own):
	
	projectile_id = own.projectile_id
	if projectile_id == -1: # we died on our own.
		return
	
	# Get the hitlist for this player
	try:	hitlist = GameLogic.globalDict['HUD']['hitlist_p%d' % (projectile_id+1)]
	except:	return # Not initialized yet.... ignore for a couble of redraws
	
	id = own.id
	new_item = (id, own.type, own.life, own.lifemax)
	
	DO_INSERT = True
	for i,item in enumerate(hitlist):
		if item[0] == id: # update existing stat?
			hitlist[i] = new_item
			DO_INSERT = False
			break
	
	# ok its not in the list, add it
	if DO_INSERT:
		hitlist.append(new_item)


# --- 
# See frank_stat_hit, this sets the hit property that triggers this script.
def main(cont):
	own = cont.getOwner()
	
	# print own.hit, 'own.hit'
	
	if own.hit==0 or own.revive_time < 1.0:
		own.hit = 0
		return
	
	# Dont do this, breaks lava death
	'''
	if own.grounded == 0:
		# trigger so will re-run
		print '\tchar: not on ground, not reacting to hit yet'
		return
	'''
	
	sens_kill = cont.getSensor('hit_detect')
	
	if not sens_kill.isPositive(): # Why would this be false??
		return
	
	own.life = life = max(own.life - own.hit, 0)
	
	own.hit = 0
	own.revive_time= 0.0
	
	
	# Update the hitlist
	update_hud(cont, own)
	
	# play sound if we have one. make sure name is sfx_*
	for actu_sound in cont.getActuators():
		if actu_sound.getName().startswith('sfx_'):
			GameLogic.addActiveActuator( actu_sound, True )
	
	
	if life == 0:
		actu_death = cont.getActuator('dead_state')
		GameLogic.addActiveActuator( actu_death, 1 )
		
		return
	"""
	actu_hit = actu_kicked = None
	for actu in cont.getActuators():
		name = actu.getName()
		if name.startswith('hit'):
			actu_hit = actu
			break
		elif name.startswith('kicked'):
			actu_kicked = actu
			break
	
	# Play Hit Anim
	print '\nSHEEP WAS HIT!!!!!\n'
	print 'own.attack_type', own.attack_type
	if own.attack_type=='kick':
		own.attack_type = ''
		if actu_kicked:
			actu_hit = actu_kicked
	
	GameLogic.addActiveActuator( actu_hit, True )
	"""
	# State switch time - stop us from switching 
	
	# Dont set a new state for a while, play recover anim
	# own.state_switch_time = -4.0
	
	actu_idle = cont.getActuator('hit_state')
	GameLogic.addActiveActuator( actu_idle, True )
