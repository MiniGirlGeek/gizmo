from time import sleep
from picamera import PiCamera
import centre
import math
import blinkt

blinkt.clear()
blinkt.set_all(255, 255, 255)
blinkt.set_brightness(1)
blinkt.show()

camera = PiCamera()
camera.start_preview()
camera.iso=10
camera.color_effects = (128,128)
camera.shutter_speed = 10000
sleep(2)

c_old = (0, 0)
for filename in camera.capture_continuous('big_images/img{counter:03d}.png', format='png'):
	pass
	'''
	c_new = centre.process_image(filename)
	print(c_new)
	if c_new:
		dx = c_new[0]-c_old[0]
		dy = c_new[1]-c_old[1]
		#print("dx:{0}, dy:{1}".format(dx, dy))
		magnitude = math.sqrt(dx**2 + dy**2)
		if magnitude > 5:
			print('magnitude:{0}, angle:{1}'.format(magnitude, math.acos(dx/magnitude)*(180/math.pi)))
			blinkt.set_all(0, 255, 0)
			blinkt.show()
		else:
			blinkt.set_all(255, 255, 255)
			blinkt.show()
		c_old = c_new'''
