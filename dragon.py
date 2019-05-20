import random
import board
import rpi_ws281x
import time
import math

#WS2812 (NeoPixel) setup
NO_LEDS = 29 #defines the number of LEDs in the chain
LED_PIN = 18 #the BCM pin the LEDs are connected to

LED_FREQ_HZ    = 800000
LED_DMA        = 10
LED_BRIGHTNESS = 255
LED_INVERT     = False
LED_CHANNEL    = 0
pixels = rpi_ws281x.Adafruit_NeoPixel(NO_LEDS, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
pixels.begin()

class Sphere:
	'''An object representing the dragon box's glowing ping pong balls'''
	def __init__(self, y, x, pix_pos, broken=False):
		self.broken = broken #must be set before colour as used by @colour.setter
		
		self.x = x #coordinate within the sphere layout
		self.y = y #coordinate within the sphere layout
		
		self.pix_pos = pix_pos #represents the WS2812 chain position for this sphere
		
		self.colour = (0, random.randint(25, 200), 0) #initially set up for flame mode, a random colour so they don't all start out the same
		self.flame_target = random.randint(25, 200) 
		self.flicker_speed = 0.5 #can adjust the speed of the flame animation
		
		self.hue = 0 #required for rainbow mode
		
		self.run_mode = self.flame
		

		'''Some of the WS2812s had one or more LEDs broken, to avoid unwanted colours
		   they were simple switched off using this flag.'''
		if self.broken:
			self.colour = (0, 0, 0)

	@property
	def colour(self):
		'''defines colour as a property of the Sphere class so behaviour
		   can be defined for when this value is set.'''
		return self._colour

	@colour.setter
	def colour(self, value):
		'''When the colour value is updated, adjusts the pixel colour to match.'''
		if not self.broken:
			self._colour = value
			self.pixcolour = rpi_ws281x.Color(int(value[0]), int(value[1]), int(value[2]))
			pixels.setPixelColor(self.pix_pos, self.pixcolour)
		else:
			'''If the pixel is broken then the sphere will ignore instructions to update it's colour
			   saves you from having to remember which pixels are broken. It also doesn't update the
			   WS2812 as there would be no point and this would waste time.'''
			self._colour = (0, 0, 0)

	def white(self):
		'''Only updates the colour if it's not already white - for example if switching between modes.'''
		if self.colour != (155, 155, 155):
			self.colour = (155, 155, 155)

	def flame(self):
		'''Defines the behavior of flame mode, each time it is called
		   it will adjust the colour of the sphere to move it closer towards
		   the target colour. Once the target colour is reached, a new target
		   colour is set. Only green has a taget value, as to keep the colours
		   firey red should always be 255 and blue should always be 0.'''

		if self.colour[1] == self.flame_target:
			#sets a new target colour
			self.flame_target = random.randint(25, 200)

		elif self.colour[1] > self.flame_target:
			#reduces value towards target colour
			self.colour = (255, self.colour[1] - self.flicker_speed, 0)

		else:
			#increases value towards target colour
			self.colour = (255, self.colour[1] + self.flicker_speed, 0)

	def cap(self, value):
		'''Caps values between 0 and 255 (valid LED brighnesses) so a cosine wave
		 can be used to generate a rainbow effect.'''
		if value > 255:
			return 255
		elif value < 0:
			return 0
		else:
			return value

	def rainbow(self):
		'''Uses 3 out of phase cosine waves to approximate a rainbow'''
		r = self.cap(255 * (math.cos(self.hue + (self.y / 2)) + 0.5))
		g = self.cap(255 * (math.cos(self.hue + (2/3) * math.pi + (self.y / 2)) + 0.5))
		b = self.cap(255 * (math.cos(self.hue + (4/3) * math.pi + (self.y / 2)) + 0.5))
		self.colour = (r, g, b)
		self.hue += math.pi / 7200


# a data structure reflective of the layout of the spheres in the real world to make it easier for me to visualise
sphere_layout = {0:[                                    Sphere(0, 0,  8)                                    ],
				 1:[                           Sphere(1, 0,  9), Sphere(1, 1,  7)                           ],
				 2:[                  Sphere(2, 0, 18), Sphere(2, 1, 10), Sphere(2, 2,  6)                  ],
				 3:[         Sphere(3, 0, 19), Sphere(3, 1, 17, broken=True), Sphere(3, 2, 11), Sphere(3, 3,  5)         ],
				 4:[Sphere(4, 0, 28), Sphere(4, 1, 20, broken=True), Sphere(4, 2, 16), Sphere(4, 3, 12), Sphere(4, 4,  4)],
				 5:[         Sphere(5, 0, 27), Sphere(5, 1, 21), Sphere(5, 2, 15), Sphere(5, 3, 13, broken=True)         ],
				 6:[                  Sphere(6, 0, 26, broken=True), Sphere(6, 1, 22), Sphere(6, 2, 14)                  ],
				 7:[                           Sphere(7, 0, 25, broken=True), Sphere(7, 1, 23)                           ],
				 8:[                                    Sphere(8, 0, 24)                                    ]}

# ran out of time to make a different class for dragon scales
scales = [Sphere(1, 0, 0), Sphere(2, 1, 1), Sphere(3, 2, 2), Sphere(4, 3, 3)]

while True:
	for row in sphere_layout:
		for sphere in sphere_layout[row]:
			sphere.run_mode() # the mode can be switched between white, rainboe and flame
	for scale in scales:
		scale.rainbow()
	pixels.show()