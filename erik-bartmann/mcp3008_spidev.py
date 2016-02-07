#!/usr/bin/python
import RPi.GPIO as GPIO # GPIO-Library
import spidev           # SPI-Dev Library
from time import sleep  # sleep importieren

class MCP3008:    
    def __init__(self, bus = 0, client = 0):
        """ Konstruktor """
        self.spi = spidev.SpiDev()
        self.spi.open(bus, client)
        
    def readAnalogData(self, channel):
        """ Liest den analogen Wert """
        if channel not in range(8):
            return -1
        rBytes = self.spi.xfer2([1, (8 + channel) << 4, 0])
        adcValue = ((rBytes[1] & 3) << 8) + rBytes[2]
        return adcValue

def main():
    mcp3008 = MCP3008() # MCP3008 Instanz generieren
    ch      = 0         # ADC-Kanalnummer
    delay   = 1         # Pausenwert
    while True:
        print mcp3008.readAnalogData(ch)
        sleep(delay)
    
if __name__ == '__main__':
    main()    