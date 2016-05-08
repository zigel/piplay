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
  
```
you need two things in order to accomplish your task:

You need a Python library that can output MIDI (e.g. python-midi or python-rtmidi)
You need a soft synth. You can use Timidity for that, which can be used as an ALSA sequencer device.
You can install timidity using apt. You have to start timidity in ALSA server mode:

timidity -iA -B2,8 -Os -EFreverb=0
This line is taken from the above link. The settings may vary, important is the -iA. The other parameters deal with buffering and disabling the reverb effect, to save CPU cycles.

You can test the timidity server by using aplaymidi:

aplaymidi -l
aplaymidi -p 65:0 somemidifile.mid
Where 65:0 has to be replaced by the MIDI sequencer that you see after running  aplaymidi -l.

On the Python side, I cannot give you much advice, except reading the docs for the python-midi package. There you also have to connect to the ALSA sequencer device from above and send your MIDI events to that port.
```

#### Further reading
 - additional timidity setup see here: https://www.raspberrypi.org/forums/viewtopic.php?f=38&t=89102
 - instruments: https://www.raspberrypi.org/forums/viewtopic.php?f=77&t=127837
 
### python-rtmidi 
- install http://trac.chrisarndt.de/code/wiki/python-rtmidi/install%20

#### requirements (bäh)
- cython: `sudo pip install Cython --install-option="--no-cython-compile"`
- libasound: `sudo apt-get install libasound2-dev`
- jack: `sudo apt-get install libjack-jackd2-dev`
 
