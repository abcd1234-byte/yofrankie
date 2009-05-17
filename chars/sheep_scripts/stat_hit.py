import GameLogic

# This file has almost an exact copy in frank.blend - frank_projectile_hit
def main(cont):
	PROJECTILE_SPEED = 5.0
	own = cont.getOwner()
	#sens = cont.getSensor('projectile_touch')
	for sens in cont.getSensors():		
		hit_ob = sens.getHitObject()
		if hit_ob:
			if hasattr(hit_ob, 'projectile'):
				s = hit_ob.getLinearVelocity()
				s = s[0]*s[0] + s[1]*s[1] + s[2]*s[2]
				# print 'hit_speed', s
				# Is this going to hit us???
				if s > PROJECTILE_SPEED:
					if hasattr(hit_ob, 'kill'):
						own.hit = max(hit_ob.kill, own.hit)
						GameLogic.bonecount+=hit_ob.kill #add the amount of health lost to the 'total broken bones' counter
					else:
						own.hit = max(1, own.hit)
			elif hasattr(hit_ob, 'kill'):
				own.hit = max(hit_ob.kill, own.hit)
