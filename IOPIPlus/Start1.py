import sys
import time
import rtmidi
from ABE_helpers import ABEHelpers
from ABE_IoPi import IoPi
from rtmidi.midiconstants import *
from threading import Thread
import RPi.GPIO as GPIO

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
    if True: #still_playing == 0:
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
    global buttonbus
    i2c_helper = ABEHelpers()
    i2c_bus = i2c_helper.get_smbus()
    sensorbus = IoPi(i2c_bus, 0x20) 
    # set both rows of pins to input mode
    sensorbus.set_port_direction(0, 0xFF)
    sensorbus.set_port_direction(1, 0xFF)
    #setup interrupts on bus 2, port 1
    buttonbus = IoPi(i2c_bus, 0x21)
    # Set all pins on the bus to be inputs with internal pull-ups enabled.
    buttonbus.set_port_pullups(1, 0xFF)
    buttonbus.set_port_direction(1, 0xFF)
    # Inverting the ports will allow a button connected to ground to register as 1 or on.
    buttonbus.invert_port(1, 0xFF)  # invert port 1 so a button press will register as 1
    # Set the interrupt polarity to be active low and mirroring enabled, so
    # INT A and INT B go low when an interrupt is triggered
    buttonbus.set_interrupt_polarity(0)
    #buttonbus.mirror_interrupts(1)
    # Set the interrupts default value to 0 so it will trigger when any of the pins on the bus change to 1
    buttonbus.set_interrupt_defaults(1, 0x00)
    # Set the interrupt type to be 0xFF for port B so an interrupt is
    # fired when the pin matches the default value
    buttonbus.set_interrupt_type(1, 0xFF)
    # Enable interrupts for all pins on the port
    buttonbus.set_interrupt_on_port(1, 0xFF)
    # reset the interrups on the IO Pi bus 
    buttonbus.reset_interrupts()

    GPIO.setmode(GPIO.BCM)
    # Set up GPIO 23 as an input. The pull-up resistor is disabled as the level shifter will act as a pull-up. 
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    # when a falling edge is detected on GPIO pin 23 the function button_pressed will be run  
    GPIO.add_event_detect(23, GPIO.FALLING, callback=hwbutton_pressed) 
    # create a function  to be called when GPIO 23 falls low

def hwbutton_pressed(channel): 
    global buttonbus
    
    portb = buttonbus.read_interrupt_status(1)
    
    # loop through each bit in the porta variable and check if the bit is 1 which will indicate a button has been pressed
    # print "interrupt"
    if 1 & portb:
        # print "bit found"
        Cycle_Instrument()
    while portb == buttonbus.read_port(1):
        time.sleep(0.01)
    
    # reset the interrupts on the bus
    
    buttonbus.reset_interrupts()

    
def Read_IOPiPorts():
    global sensorbus    
    port0 = sensorbus.read_port(0)
    port1 = sensorbus.read_port(1)
    return port0 + (port1 << 8)
    
def Init_Others():
    global last_string_state
    global instr_num
    instr_num = 0
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

def probe_note():
    global G_MIDIOUT
    note = 60
    G_MIDIOUT.send_message(note_off(note))
    G_MIDIOUT.send_message(note_on(note))
    time.sleep(1) 
    G_MIDIOUT.send_message(note_off(note))


def Select_Instrument(Instr):
    global G_MIDIOUT
    msg = [PROGRAM_CHANGE, Instr] 
    G_MIDIOUT.send_message(msg)
    Thread(target=probe_note).start()

def Cycle_Instrument():
    global instr_num
    instr_num += 1
    print "Instrument", instr_num
    Select_Instrument(instr_num)
        
def Start_All():
    print "Start Others"
    Init_Others()
    print "Start IOPi"
    Init_IOPi()
    print "Init midi"
    Init_Midi()
    Select_Instrument(0)
    print "Start Loop"
    Main_Loop()
    
Start_All()
    
