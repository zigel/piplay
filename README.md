# piplay
## Buy list
- [x] 1x MCP3008
- [x] 12+ LDR 10mm or 12mm
  - http://www.pollin.de/shop/dt/NDAyOTc4OTk-/Bauelemente_Bauteile/Aktive_Bauelemente/Optoelektronik/Fotowiderstand_PFW1251_12_mm_5_Stueck.html 
- [ ] 16x 10kO Resistors
- [ ] kabel schwarz, rot, grün

## TODO
- MCP3008
  - [x] test spidev 
  - [x] optimize spidev bytes - **doesn't work** with less than 3 bytes input
- IO PI Plus
  - [x] solder connectors 
  - [x] try LDRs with pulldown
  - [ ] try interrupts

## Steps
- install spidev (from http://raspberrypi-aa.github.io/session3/spi.html)
```
git clone git://github.com/doceme/py-spidev
cd py-spidev
sudo python setup.py install
```
## Install midi

### Timidity
- Install timidity https://packages.debian.org/jessie/sound/timidity 
 https://www.howtoinstall.co/en/debian/jessie/main/timidity/ 
  - `sudo apt-get install timidity`
- Start timidity in server mode and test: http://raspberrypi.stackexchange.com/questions/7359/python-synth-with-raspberry 
  - `timidity -iA -B2,8 -Os -EFreverb=0` (somewhere in [screen](http://ss64.com/bash/screen.html) ?)
-  Test timidity `aplaymidi -l`
```
aplaymidi -p 65:0 somemidifile.mid
Where 65:0 has to be replaced by the MIDI sequencer that you see after running  aplaymidi -l
``` 


#### Further reading
 - additional timidity setup see here: https://www.raspberrypi.org/forums/viewtopic.php?f=38&t=89102
 - instruments: https://www.raspberrypi.org/forums/viewtopic.php?f=77&t=127837
 - __connecting ports__: https://chivalrytimberz.wordpress.com/ 
 
### python-rtmidi 
- install http://trac.chrisarndt.de/code/wiki/python-rtmidi/install%20

#### requirements (bäh)
- cython: `sudo pip install Cython --install-option="--no-cython-compile"`
- libasound: `sudo apt-get install libasound2-dev`
- jack: `sudo apt-get install libjack-jackd2-dev`
 
### first working samle
```
import time
import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

print available_ports

if available_ports:
    midiout.open_port(1)
else:
    midiout.open_virtual_port("My virtual output")

note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
note_off = [0x80, 60, 0]
midiout.send_message(note_on)
time.sleep(0.5)
midiout.send_message(note_off)

del midiout
``` 
