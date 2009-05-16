# This file has almost an exact copy in sheep.blend - sheep_sense_hit
'''
Run when we touch a kill or projectile object,
this sets own.hit which the 'frank_health' script then deals with.
'''
import GameLogic

def main(cont):
	PROJECTILE_SPEED = 5.0
	
	own = cont.getOwner()
	
	HIT_PLAYED = False
	try:	actu_hit = cont.getActuator('sfx_hit')
	except:	HIT_PLAYED = True
		
		
	
	#sens = cont.getSensor('projectile_touch')
	for sens in cont.getSensors():		
		hit_ob = sens.getHitObject()
		if not hit_ob:
			continue
		
		if hasattr(hit_ob, 'projectile') and hit_ob.projectile_id != own.id:
			s = hit_ob.getLinearVelocity()
			s = s[0]*s[0] + s[1]*s[1] + s[2]*s[2]
			print 'hit_speed', s
			# Is this going to hit us???
			if s > PROJECTILE_SPEED:
				if hasattr(hit_ob, 'kill'):
					own.hit = max(hit_ob.kill, own.hit)
				else:
					own.hit = max(1, own.hit)
			
		elif hasattr(hit_ob, 'kill'):
			own.hit = max(hit_ob.kill, own.hit)
	 		
			# Play the hit sound if we havnt played it and if its not liquid
			if HIT_PLAYED == False and not hasattr(hit_ob, 'liquid'):
				GameLogic.addActiveActuator( actu_hit, True)
