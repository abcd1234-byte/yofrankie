'''
sets the key text for the help screen
'''

import GameKeys
import GameLogic

def main(cont):
	own = cont.getOwner()
	
	try:	conf = GameLogic.globalDict['CONFIG']
	except:	conf = GameLogic.globalDict['CONFIG'] = {}
	
	children = [(ob.getName(), ob) for ob in own.getChildren()]
	children.sort()
	
	obs_p1 = [ pair[1] for pair in children if '_p1' in pair[0] ]
	obs_p2 = [ pair[1] for pair in children if '_p2' in pair[0] ]
	
	
	if not conf:
		for ob in obs_p1:		ob.Text = 'debug'
		for ob in obs_p2:		ob.Text = 'debug'
		return
	
	# Override key text
	joy_p1 = cont.getSensor('joy_test_p1').isConnected()
	joy_p2 = cont.getSensor('joy_test_p2').isConnected()	
	
	# Always do player 1
	keys_p1 = []
	keys_p2 = []
	
	
	if not joy_p1:
		for item in conf.iteritems():
			if item[0].startswith('KEY_') and item[0].endswith('_P1'):
				keys_p1.append( item )
	
		keys_p1.sort()
		
	if not joy_p2:
		for item in conf.iteritems():
			if item[0].startswith('KEY_') and item[0].endswith('_P2'):
				keys_p2.append( item )
			
		keys_p2.sort()
	
	
	text_p1 = ['player 1 keys']
	text_p2 = ['player 2 keys']
	
	for keys, text, obs, joy_connected in [(keys_p1, text_p1, obs_p1, joy_p1), (keys_p2, text_p2, obs_p2, joy_p2)]:
		if joy_connected:
			text.append( 'using joystick' )
		else:
			for key, value in keys:
				# KEY_UP_P1 -> up
				name = key.split('_')[1].lower()
				val = GameKeys.EventToString(value).replace('KEY', '').lower()
				text.append('%s - %s' % (name, val))
		
		for i, line in enumerate(text):
			obs[i].Text = line

