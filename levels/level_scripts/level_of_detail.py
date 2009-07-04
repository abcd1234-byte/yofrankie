# remove objects based on detail setting.
import GameLogic
def main(cont):
	own = cont.owner
	sce = GameLogic.getCurrentScene()
	
	conf = GameLogic.globalDict.get('CONFIG', {})
	detail = conf.get('GRAPHICS_DETAIL', 2)
	
	# detail is a pref, can be 0,1,2: 2 is high detail, dont do anything

	for ob in sce.objects:
		lod_level= ob.get('lod_level')
		end = False
		
		if detail==0:
			end = (lod_level < 2)
		elif if detail==1:
			end = (lod_level < 1)
		
		if end:		ob.endObject()
		else:		del ob['lod_level']
		
	own.endObject()
