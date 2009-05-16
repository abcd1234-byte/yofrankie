'''
This script restores frankie to his original location
restores properties and updates the hud.
'''
import GameLogic

def main(cont):
	own = cont.getOwner()
	
	# If somthing is carrying us. tell it to not bother anymore.
	parent = own.getParent()
	if parent:
		if hasattr(parent, 'carrying'):
			parent.carrying = 0
		else:
			print '\twarning, parented to a non "carrying" object. should never happen'
		
		own.removeParent()
		
	own.setPosition( [float(num) for num in own.orig_pos.split()] )
	own.setLinearVelocity([0,0,0], 1)
	
	props = GameLogic.globalDict['PROP_BACKUP'][own.id]
	
	# We backed these up, see frank_init
	for prop, value in props.iteritems():
		setattr(own, prop, value)
	
	# Update the HUD
	hud_dict = GameLogic.globalDict['HUD']
	if own.id == 0:	hud_dict['life_p1'] = own.life
	else:			hud_dict['life_p2'] = own.life
	
