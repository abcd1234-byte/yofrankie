'''
Detect if we have any joysticks and
remove the keyconfig objects if we have them plugged in
'''
import GameLogic

def main(cont):
	own = cont.owner
	
	# Only run once
	if not cont.sensors['joy_opts_init'].positive:
		return
	
	# Note, after entering key config, this 
	joy_p1_connected = cont.sensors['joy_detect_p1'].connected
	joy_p2_connected = cont.sensors['joy_detect_p2'].connected
	
	if joy_p1_connected:
		cont.activate('end_keys_p1')
		cont.activate('set_joy_message_p1')
		
	if joy_p2_connected:
		cont.activate('end_keys_p2')
		cont.activate('set_joy_message_p2')
	
	cont.activate('remove_joy_detect')
