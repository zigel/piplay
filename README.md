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
- 
