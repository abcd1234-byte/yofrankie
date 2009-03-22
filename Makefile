BLENDER = blender
PYTHON = python
SVN = svn
PACKAGE_DIR = ./package

all:
	# Copy files into a package dir
	rm -rf $(PACKAGE_DIR)
	
	# copy with svn export or normal copy if this is not a checkout
	if test -d .svn; \
	then $(SVN) export . $(PACKAGE_DIR); \
	else mkdir ./package; cp -pR audio chars effects hud levels menus props textures $(PACKAGE_DIR)/; \
	fi
	# end shell command
	
	
	# Convert images, correct blendfile paths
	# TODO - this is broken with 2.48a, because blend files saved have no G.curscreen
	# $(PYTHON) dist/imagefile_compress.py $(BLENDER) $(PACKAGE_DIR)
	
	# Compress all blendfiles
	$(PYTHON) dist/blendfile_gzip.py $(PACKAGE_DIR)
	
	
	