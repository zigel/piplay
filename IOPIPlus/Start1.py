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
    global G_MIDIOUT
    global G_MIDIPORT
    
    G_MIDIOUT = rtmidi.MidiOut()
    G_MIDIOUT.open_port(1) if G_MIDIOUT.get_ports() else  G_MIDIOUT.open_virtual_port("My virtual output")

def play_string(string):
    global G_MIDIOUT
    print "play " + str(string + 1)
    note = NoteFromString(string)
    G_MIDIOUT.send_message(note_on(note))
    time.sleep(2) 
    still_playing = 1 - (1 & (last_string_state << string))
    # print string, last_string_state << string, 1 & (last_string_state << string), still_playing
    if still_playing == 0:
        G_MIDIOUT.send_message(note_off(note))
        print "-play " + str(string + 1)

def Change_String(string, State):
    global G_MIDIOUT
    note = NoteFromString(string)
    if (State == 0):
        # G_MIDIOUT.send_message(note_on(note))
        # print "play " + str(string + 1)
        Thread(target=play_string, args=(string,)).start()
    else:
        G_MIDIOUT.send_message(note_off(note))
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
        for b in range(0, 12):
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
        time.sleep(0.05) 

def Select_Instrument(Instr):
    global G_MIDIOUT
    msg = [PROGRAM_CHANGE, Instr] 
    G_MIDIOUT.send_message(msg)
    
        
def Start_All():
    print "Start Others"
    Init_Others()
    print "Start IOPi"
    Init_IOPi()
    print "Init midi"
    Init_Midi()
    Select_Instrument(7)
    print "Start Loop"
    Main_Loop()
    
Start_All()
    
