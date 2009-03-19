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
		

if change:
	filename = Blender.Get('filename')
	print "Saving", filename
	Blender.Save(filename, True) # True==Overwrite

# Incase were not running in background mode
Blender.Quit()
