#!/usr/bin/env python
#
# test_midiin_callback.py
#
"""Shows how to use a MidiOut instance as a context manager."""

import time
import rtmidi

from rtmidi.midiconstants import *

def note_on(note):
    return [NOTE_ON, note, 127]

def note_off(note):
    return [NOTE_OFF, note, 0]

C4 = 60
D4 = 62
#Ccis = 61
E4 = 64
F4 = 65
G4 = 67
A4 = 69 
H4 = 71

Entchen = [C4, D4, E4, F4, G4, G4, A4, A4, A4, A4, G4, A4, A4, A4, A4, G4]


Entchen_Mit_Zeiten = { 
    "Noten":  [C4, D4, E4, F4, G4, G4, A4, A4, A4, A4, G4, A4, A4, A4, A4, G4],
    "Zeiten": [0.5,0.5,0.5,0.5, 1, 1, 0.5,0.5,0.5,0.5,  2, 0.5,0.5,0.5,0.5, 2],
}

def play_simple_list(L):
    for n in L:
        midiout.send_message(note_on(n))
        time.sleep(0.5)
        midiout.send_message(note_off(n))

def spiel_mit_zeiten(Notenheft):
    dauer_einer_note_in_sec = 0.1
    noten = Notenheft["Noten"]
    zeiten = Notenheft["Zeiten"]
    anzahl = len(noten)
    for i in range(0, anzahl):
        die_note = noten[i]
        die_zeit = zeiten[i]
        midiout.send_message(note_on(die_note))
        time.sleep(die_zeit * dauer_einer_note_in_sec)
        midiout.send_message(note_off(die_note))



midiout = rtmidi.MidiOut()

with (midiout.open_port(1) if midiout.get_ports() else
        midiout.open_virtual_port("My virtual output")):
    
    # play_simple_list(Entchen)
    spiel_mit_zeiten(Entchen_Mit_Zeiten)
    
    # midiout.send_message(note_on(C))
    # time.sleep(1)
    # midiout.send_message(note_on (A))
    # time.sleep(4)
    # midiout.send_message(note_off(C))
    # time.sleep(1)
    # midiout.send_message(note_off(C))

del midiout
