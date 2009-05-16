# Better only keep a subset of our props

'''
when touching a "portal" property object, use its properties to move to its target.
possible targets are object, scene or blendfile (or a mix)
When loading scenes or blendfiles, "frank_init" scripts check for the portal settings and finish off the positioning.
'''

import GameLogic

def backupProps(own):
	# We could reset others but these are likely to cause problems
	PROPS = GameLogic.globalDict['PROP_BACKUP'][own.id]
	# We backed these up, see frank_init
	# Only backup "life" and inventory -> "item_*"
	PROPS['life'] = own.life
	for propName in own.getPropertyNames():
		if propName.startswith('item_'):
			PROPS[propName] = getattr(own, propName)


def main(cont):
	own = cont.getOwner()
	globalDict = GameLogic.globalDict
	
	portal_ob = cont.getSensor('portal_touch').getHitObject()
	
	if not portal_ob:
		return
	
	sce = GameLogic.getCurrentScene()
	target_name = portal_ob.portal
	
	# incase the portal was set before
	# we dont want to use an invalid value
	try:	del globalDict['PORTAL_OBNAME']
	except:	pass
	
	try:	del globalDict['PORTAL_SCENENAME']
	except:	pass
	
	blend_name = scene_name = ''


	if hasattr(portal_ob, 'portal_blend'):	
		blend_name = portal_ob.portal_blend # No way to check if this really matches up to a scene
	
	if hasattr(portal_ob, 'portal_scene'):
		scene_name = portal_ob.portal_scene # No way to check if this really matches up to a scene
	
	if blend_name:
		# todo, allow blend AND scene switching. at the moment can only do blend switching.
		set_blend_actu = cont.getActuator('portal_blend')
		set_blend_actu.setFile( blend_name )
		
		try:	del globalDict['PLAYER_ID'] # regenerate ID's on restart
		except:	pass
		
		if target_name:
			globalDict['PORTAL_OBNAME'] = 'OB' + target_name
		
		if scene_name:
			globalDict['PORTAL_SCENENAME'] = scene_name
				
		# Backup props
		backupProps(own)
				
		GameLogic.addActiveActuator(set_blend_actu, True)
		
	elif scene_name:
		# portal_ob
		set_scene_actu = cont.getActuator('portal_scene')
		set_scene_actu.setScene( scene_name )
		
		try:	del globalDict['PLAYER_ID'] # regenerate ID's on restart
		except:	pass
		
		if target_name:
			globalDict['PORTAL_OBNAME'] = 'OB' + target_name
		
		# Backup props
		backupProps(own)
		
		GameLogic.addActiveActuator(set_scene_actu, True)
	else:
		# Simple, only move to the portal.
		try:
			target_ob = sce.getObjectList()['OB'+target_name]
		except:
			print 'Oops: portal switch error,', target_name, 'object is not in the scene'
			return
		
		# We may be gliding, make sure there is no timeoffset
		own_rig = cont.getSensor('rig_linkonly').getOwner() # The rig owns this! - cheating way ti get the rig/
		own_rig.timeOffset = own_rig.defTimeOffset
		
		own.setPosition( target_ob.getPosition() )
		own.setOrientation( target_ob.getOrientation() )
		own.setLinearVelocity([0,0,0])
		
		# set the state incase we are climbing or somthing
		set_state_actu = cont.getActuator('fall_state_switch')
		GameLogic.addActiveActuator(set_state_actu, True)
