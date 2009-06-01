
def main(cont):
	own = cont.owner
	text = own.parent['portal_blend']
	
	if 'level_selector' in text:
		own['Text'] = 'extra levels'
		return
	
	# only needed for the other level selctor
	# text = text.replace('minilevel_', '')
	
	# Nice formatting from filename 
	text = text.split('.')[0].lower() # remove extension
	
	for c in '-_/':
		text = text.replace(c, ' ')
	
	# Capitalize first letters
	# ...Secodn thaughts, lets not, our upper case
	#    letters are crap
	'''
	text_split = text.split()
	for i, word in enumerate(text_split):
		text_split[i] = word[:1].upper() + word[1:]
	
	text = ' '.join(text_split)
	'''
	
	own['Text'] = text
