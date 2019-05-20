from gpiozero import DigitalInputDevice, DigitalOutputDevice
import threading

#####################
# Button Connection #
#####################

output_pins = [2, 3]          # A list containing the pins each output row is connected to
input_pins  = [4, 17, 27, 22] # A list containing the pins each input row is connected to

outputs = [] # A list to store the setup GPIOzero objects - populated below
inputs  = [] # A list to store the setup GPIOzero objects - populated below

for pin in output_pins:
	outputs.append(DigitalOutputDevice(pin))

for pin in input_pins:
	inputs.append(DigitalInputDevice(pin))

last_button_pressed  = None

########################
# Interrupt on a timer #
########################

def button_isr():
	global last_button_pressed

	x = 0
	for output_pin in outputs:
		output_pin.on()

		last_button_pressed = None
		y = 0
		for input_pin in inputs:
			if input_pin.value:
				last_button_pressed = (x, y)
				print(i)
			y += 1
		x += 1
		output_pin.off()

	threading.Timer(0.2, button_isr).start()

button_isr()

