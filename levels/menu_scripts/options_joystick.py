'''
Detect if we have any joysticks and
remove the keyconfig objects if we have them plugged in
'''
import GameLogic

def main(cont):
	own = cont.getOwner()
	
	# Only run once
	if not cont.getSensor('joy_opts_init').isPositive():
		return
	
	# Note, after entering key config, this 
	
	joy_p1_connected = cont.getSensor('joy_detect_p1').isConnected()
	joy_p2_connected = cont.getSensor('joy_detect_p2').isConnected()
	
	if joy_p1_connected:
		GameLogic.addActiveActuator( cont.getActuator('end_keys_p1'), True)
		GameLogic.addActiveActuator( cont.getActuator('set_joy_message_p1'), True)
		
	if joy_p2_connected:
		GameLogic.addActiveActuator( cont.getActuator('end_keys_p2'), True)
		GameLogic.addActiveActuator( cont.getActuator('set_joy_message_p2'), True)
	
	GameLogic.addActiveActuator( cont.getActuator('remove_joy_detect'), True)
