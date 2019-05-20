import PIL
from PIL import Image
import numpy as np
from math import floor

def get_centre(image):
	'''returns the average x and y postition of all the black dots'''
	width, height = image.size
	x_total = 0
	y_total = 0
	x = 0
	y = 0
	total = 0

	for pixel in image.getdata():
		if x == width:
			x = 0
			y += 1
		if pixel != (255, 255, 255, 255):
			x_total += x
			y_total += y
			total += 1
		x += 1
	try:
		centre = (x_total // total, y_total // total)
	except:
		centre = False
	return centre

threshold = 50
rescale = 0.6

def process_image(filename):
	#opening the image
	img = Image.open(filename)
	#thresholding the image, deciding if a pixel is a dot (black or white) or not
	img_ = PIL.Image.eval(img, lambda a: 255 if a > threshold else 0)
	#reducing the image size to reduce processing time
	img_ = img_.crop((270, 130, 505, 365))
	#reducing the image resolution to reduce processing time
	img_ = img_.resize((120, 120))
	#saving the new image
	img_.save(filename[:-4]+'_.png')
	#finding the center of the dot pixels
	c = get_centre(img_)
	return c