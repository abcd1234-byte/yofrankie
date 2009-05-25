'''
Detect if we have any joysticks and set a message
for the main menu
'''
import GameLogic

def main():
	cont = GameLogic.getCurrentController()
	own = cont.getOwner()
	
	# Only run once
	if not cont.getSensor('joy_text_init').isPositive():
		return
	
	joy_p1_connected = cont.getSensor('joy_detect_p1').isConnected()
	joy_p2_connected = cont.getSensor('joy_detect_p2').isConnected()
	
	if joy_p1_connected and joy_p2_connected:
		own.Text = 'Two joysticks found'
	elif joy_p1_connected:
		own.Text = 'one joystick found'
	else:
		own.Text = 'no joysticks found'
	
