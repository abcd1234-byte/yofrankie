# This script must run inside blender
import Blender
import bpy


def replace_ext(path, ext):
	return '.'.join( path.split('.')[:-1] ) + '.' + ext

change = False

for i in bpy.data.images:
	if i.lib==None:
		filename = i.filename
		filename_abs = Blender.sys.expandpath(filename)
		
		if not Blender.sys.exists(filename_abs):
			filename_jpg = replace_ext(filename_abs, 'jpg')
			if Blender.sys.exists(filename_jpg):
				print "\tfixed path", filename_jpg
				i.filename = replace_ext(filename, 'jpg')
				change = True

filename = Blender.Get('filename')

if change:
	# Workaround for G.curscreen being null
	# in 2.49 this crashes in BG mode
	# Blender.Window.SetScreen(Blender.Window.GetScreens()[0])
	print "Saving", filename
	Blender.Save(filename, True) # True==Overwrite
else:
	print "No Changes", filename
# Incase were not running in background mode
# Blender.Quit()
