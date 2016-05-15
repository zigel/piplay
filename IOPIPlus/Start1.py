import sys
import time
import rtmidi
from ABE_helpers import ABEHelpers
from ABE_IoPi import IoPi


def NoteFromString(StringNum):
    return 60 + stringNum

def Init_IOPi():
    global sensorbus    
    i2c_helper = ABEHelpers()
    i2c_bus = i2c_helper.get_smbus()
    sensorbus = IoPi(i2c_bus, 0x20) 
    # set both rows of pins to input mode
    sensorbus.set_port_direction(0, 0xFF)
    sensorbus.set_port_direction(1, 0xFF)
    
def Read_IOPiPorts():
    global sensorbus    
    port0 = sensorbus.read_port(0)
    port1 = sensorbus.read_port(1)
    return port0 + (port1 << 8)
    
def Init_Others():
    global last_string_state
    last_string_state = 0

def Check_Strings():
    global last_string_state
    string_state = Read_IOPiPorts()
    if string_state != last_string_state:
        print "*" * 16
        # print "{0:b}".format(string_state)
        change_line = ""
        for b in range(0, 16):
            mask = 1 << b
            oldbit = last_string_state & mask
            newbit = string_state & mask
            if oldbit != newbit:
                newbit = newbit >> b
                change_line += str(newbit)
            else:
                change_line += '-'
            Change_Note (b, newbit)
        print change_line 
        last_string_state = string_state
        
def Change_Note(Note, State):
    pass
        
def Main_Loop():
    while True:
        Check_Strings()
        time.sleep(0.1) 

def Start_All():
    print "Start IOPi"
    Init_IOPi()
    print "Start Others"
    Init_Others()
    print "Start Loop"
    Main_Loop()
    
Start_All()
    
