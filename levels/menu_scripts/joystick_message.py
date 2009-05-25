'''
Detect if we have any joysticks and set a message
for the main menu
'''
import GameLogic

def main(cont):
	own = cont.owner
	
	# Only run once
	if not cont.sensors['joy_text_init'].positive:
		return
	
	joy_p1_connected = cont.sensors['joy_detect_p1'].connected
	joy_p2_connected = cont.sensors['joy_detect_p2'].connected
	
	if joy_p1_connected and joy_p2_connected:
		own.Text = 'Two joysticks found'
	elif joy_p1_connected:
		own.Text = 'one joystick found'
	else:
		own.Text = 'no joysticks found'
