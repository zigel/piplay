#!/usr/bin/python
"""
================================================
ABElectronics IO Pi 32-Channel Port Expander - Tutorial 1
Version 1.1 Created 10/05/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format

Requires python smbus to be installed: sudo apt-get install python-smbus
run with: sudo python tutorial1.py
================================================

This example uses the write_pin and writePort methods to switch pin 1 on
and off on the IO Pi.
"""
from ABE_helpers import ABEHelpers
from ABE_IoPi import IoPi
import time

i2c_helper = ABEHelpers()
i2c_bus = i2c_helper.get_smbus()

sensorbus = IoPi(i2c_bus, 0x20)
# ledbus = IoPi(i2c_bus, 0x20)

# sensorbus.set_pin_direction(1, 1)  # set pin 1 as an input

# ledbus.set_pin_direction(8, 0)  # set pin 8 as an output

# ledbus.write_pin(8, 0)  # turn off pin 8

# print "turn off pin 8"

# sensorbus.set_pin_pullup(1, 1)  # enable the internal pull-up resistor on pin 1

# sensorbus.invert_pin(1, 1)  # invert pin 1 so a button press will register as 1

# sensorbus.set_port_direction(0, 0xFF)
# sensorbus.set_port_pullups(0, 0xFF)
# sensorbus.invert_port(0, 0xFF)

sensorbus.set_port_direction(1, 0xFF)
# sensorbus.set_port_pullups(1, 0xFF)
# sensorbus.invert_port(1, 0xFF)


while True:
    print sensorbus.read_port(1)
    time.sleep(0.5) 
    # if sensorbus.read_pin(1) == 1:  # check to see if the button is pressed
        # print 'button pressed'  # print a message to the screen
        # # ledbus.write_pin(8, 1)  # turn on the led on pin 8
        # time.sleep(2)  # wait 2 seconds
    # else:
        # # ledbus.write_pin(8, 0)  # turn off the led on pin 8
        # pass
