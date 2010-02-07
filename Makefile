# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ##### END GPL LICENSE BLOCK #####

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
	$(PYTHON) dist/imagefile_compress.py $(BLENDER) $(PACKAGE_DIR)
	
	# Compress all blendfiles
	$(PYTHON) dist/blendfile_gzip.py $(PACKAGE_DIR)
	
	
	