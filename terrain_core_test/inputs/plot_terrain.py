''' 
File - plot_terrain.py
Author - Miles A. Curry (mcurry@ucar.edu)
Date - April 2019


'''

import os
import sys
import argparse

from netCDF4 import Dataset

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap

from mpas_patches import get_mpas_patches
    
parser = argparse.ArgumentParser()

parser.add_argument('file', 
                    type=str, 
                    help='''File you want to plot from''')
parser.add_argument('-v',
                    '--var', 
                    type=str,
                    default='pressure',
                    help='''Variable you want to plot from that file''')

args = parser.parse_args()
variable = args.var
file = args.file

# Open the NetCDF file and pull out the var at the given levels.
# Check to see if the mesh contains the variable
if not os.path.isfile(file):
    print("That file was not found :(")
    sys.exit(-1)

# Open the mesh using NetCDF4 Dataset.
mesh = Dataset(os.path.join(file), 'r')

# Pull the variable out of the mesh. Now we can manipulate it any way we choose
# do some 'post-processing' or other meteorological stuff
terrain = mesh.variables['ter']

# Create or get the patch file for our current mesh
patch_collection = get_mpas_patches(mesh, pickleFile=None)

# Initalize Basemap
bmap = Basemap(projection='cyl', 
               llcrnrlat=-90,
               urcrnrlat=90,
               llcrnrlon=-180,
               urcrnrlon=180,
               resolution='l')


color_map = cm.gist_earth
style = 'ggplot'

'''
Make plots at vertical levels that is specified the range below, not this will
be vertical plots, 0, 1, 2, 3, and 4 and for all the times in this mesh file
(if there are any).
'''
fig = plt.figure()
ax = plt.gca()

bmap.drawcoastlines()

bmap.drawparallels(range(-90, 90, 30), 
                   linewidth=1, 
                   labels=[1,0,0,0],
                   color='b')
bmap.drawmeridians(range(-180, 180, 45),
                  linewidth=1, 
                  labels=[0,0,0,1],
                  color='b',
                  rotation=45)

patch_collection.set_array(terrain[:])
patch_collection.set_edgecolors('face')         # No Edge Colors
patch_collection.set_antialiaseds(False)    # Blends things a little
patch_collection.set_cmap(color_map)        # Select our color_map

# Now apply the patch_collection to our axis (ie plot it)
ax.add_collection(patch_collection)

cbar = plt.colorbar(patch_collection)
cbar.set_label('Meters (M)')


# Create the title as you see fit
plt.title('Terrain (Meters)')
plt.style.use(style) # Set the style that we choose above

plt.savefig('terrain.pdf')
patch_collection.remove()
plt.close(fig)
