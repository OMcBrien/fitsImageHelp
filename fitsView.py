from astropy.io import fits
import astropy.visualization as aviz
import numpy as np
import matplotlib.pyplot as plt
import sys
import getopt

usage = """
Usage: python fitsView.py -h -l <list file> -f <file name>

Options:
-h, show this help message
-l <list file>, specify list of .fits files to view
-f <file name>, specify single file to view
"""

argv = sys.argv[1:]

try:
	opts, args = getopt.getopt(argv, 'h,l:,f:')
# 	print('opts = ', opts)
# 	print('args = ', args)
except getopt.GetoptError:
	sys.exit('\nIncorrect usage.\nPlease run "python fitsView.py -h" for help.\n')

dolist = False
dofile = False

for o, a in opts:
	if o == '-h':
		print(usage)
		sys.exit()
	if o == '-l':
# 		print(a)
		listfile = a
		fileread = open(listfile, 'r')
		files_to_read = fileread.read().splitlines()
		dolist = True
	if o == '-f':
# 		print(a)
		filename = a
		dofile = True

fig = plt.figure(figsize = (10,8))

if dofile:

	fits_data = fits.getdata(filename)
	norm = aviz.ImageNormalize(fits_data,  interval=aviz.ZScaleInterval())
	
	plt.imshow(fits_data, cmap='gray', norm = norm)
	plt.colorbar()
	plt.title(filename)
	
	
elif dolist:
	
	num_plots = len(files_to_read)
	
	if num_plots < 4:
		num_columns = 2
	else:
		num_columns = int(np.floor(np.sqrt(num_plots)))
	
	num_rows = num_plots // num_columns
	num_rows += num_plots % num_columns
	
	plot_position = range(1, num_plots + 1)
	
	for i in range(num_plots):
		ax = fig.add_subplot(num_rows, num_columns, plot_position[i])
		
		fits_data = fits.getdata(files_to_read[i])
		norm = aviz.ImageNormalize(fits_data,  interval=aviz.ZScaleInterval())
		
		plt.imshow(fits_data, cmap='gray', norm = norm)
		plt.colorbar(ax = ax)
		plt.title(files_to_read[i])
		
plt.tight_layout()
plt.show(fig)
	