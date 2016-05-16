import sys
import time
import rtmidi
from ABE_helpers import ABEHelpers
from ABE_IoPi import IoPi
from rtmidi.midiconstants import *
from threading import Thread

def NoteFromString(StringNum):
    return 60 + StringNum

def Init_Midi():
    global midiout
    midiout = rtmidi.MidiOut()
    midiout.open_port(1) if midiout.get_ports() else  midiout.open_virtual_port("My virtual output")

def play_string(string):
    global midiout
    print "play " + str(string + 1)
    note = NoteFromString(string)
    midiout.send_message(note_on(note))
    time.sleep(2) 
    midiout.send_message(note_off(note))
    print "-play " + str(string + 1)

def Change_String(string, State):
    global midiout
    note = NoteFromString(string)
    if (State == 0):
        # midiout.send_message(note_on(note))
        # print "play " + str(string + 1)
        Thread(target=play_string, args=(string,)).start()
    else:
        midiout.send_message(note_off(note))
        print "stop " + str(string + 1)
    pass

def note_on(note):
    return [NOTE_ON, note, 127]

def note_off(note):
    return [NOTE_OFF, note, 0]

    
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
        # print "*" * 16
        # print "{0:b}".format(string_state)
        _change_line = ""
        _new_line = ""
        for b in range(0, 16):
            mask = 1 << b
            oldbit = last_string_state & mask
            newbit = string_state & mask
            _new_line += str(newbit >> b)
            if oldbit != newbit:
                newbit = newbit >> b
                _change_line += str(newbit)
                Change_String (b, newbit)
            else:
                _change_line += '-'
        print _change_line 
        print _new_line 
        last_string_state = string_state
        
        
def Main_Loop():
    while True:
        Check_Strings()
        time.sleep(0.1) 

def Start_All():
    print "Start Others"
    Init_Others()
    print "Start IOPi"
    Init_IOPi()
    print "Init midi"
    Init_Midi()
    print "Start Loop"
    Main_Loop()
    
Start_All()
    
