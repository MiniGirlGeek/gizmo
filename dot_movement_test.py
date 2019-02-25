import PIL
from PIL import Image
import numpy as np
from math import floor

im1 = Image.open('test3.png')
im2 = Image.open('test4.png')

def get_centre(image):
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

	centre = (x_total // total, y_total // total)
	return centre

threshold = 50

im1_ = PIL.Image.eval(im1, lambda a: 255 if a > threshold else 0)
im1_.save('test3_.png')
c1 = get_centre(im1_)
print(c1)

im2_ = PIL.Image.eval(im2, lambda a: 255 if a > threshold else 0)
im2_.save('test4_.png')
c2 = get_centre(im2_)
print(c2)

direction = (c2[0] - c1[0], c2[1] - c1[1])
print(direction)