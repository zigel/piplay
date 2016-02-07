import time;
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # GPIO-Pin Bezeichnungen verwenden
GPIO.setwarnings(False) # Warnungen deaktivieren

def readAnalogData(adcChannel, SCLKPin, MOSIPin, MISOPin, CSPin, delay):
    """ Funktionsdefinition """
    # Negative Flanke des CS-Signals generieren
    GPIO.output(CSPin,   GPIO.HIGH)
    GPIO.output(CSPin,   GPIO.LOW)
    GPIO.output(SCLKPin, GPIO.LOW)   
    sendCMD = adcChannel
    sendCMD |= 0b00011000 # Entspricht 0x18 (1: Startbit, 1: Single/ended)
    # Senden der Bitkombination (Es finden nur 5 Bits Beruecksichtigung)
    for i in range(5):
        if(sendCMD & 0x10): # Bit an Position 4 pruefen.
            GPIO.output(MOSIPin, GPIO.HIGH)
        else:
            GPIO.output(MOSIPin, GPIO.LOW)
        # Negative Flanke des Clock-Signals generieren
        GPIO.output(SCLKPin, GPIO.HIGH)
        GPIO.output(SCLKPin, GPIO.LOW)
        sendCMD <<= 1 # Bitfolge eine Position nach links schieben
    # Empfangen der Daten des AD-Wandlers
    adcValue = 0 # Reset des gelesenen Wertes
    for i in range(11):
        # Negative Flanke des Clock-Signals generieren
        GPIO.output(SCLKPin, GPIO.HIGH)
        GPIO.output(SCLKPin, GPIO.LOW)
        adcValue <<= 1 # Bitfolge 1 Position nach links schieben
        if(GPIO.input(MISOPin)):
            adcValue |=0x01
    time.sleep(delay) # Kurze Pause
    return adcValue

def setupGPIO(SCLKPin, MOSIPin, MISOPin, CSPin):
    """ GPIO-Pin Setup """
    GPIO.setup(SCLKPin, GPIO.OUT)
    GPIO.setup(MOSIPin, GPIO.OUT)
    GPIO.setup(MISOPin, GPIO.IN)
    GPIO.setup(CSPin,   GPIO.OUT)

# Variablendefinition
ADCChannel   = 0   # AD-Kanal
SCLK         = 18  # Serial-Clock
MOSI         = 24  # Master-Out-Slave-In
MISO         = 23  # Master-In-Slave-Out
CS           = 25  # Chip-Select
PAUSE        = 0.5 # Anzeigepause
THRESHOLD    = 3   # Toleranzwert
actual_value = 0   # Speichert aktuellen analogen Messwert
prev_value   = 0   # Speichert vorherigen analogen Messwert

setupGPIO(SCLK, MOSI, MISO, CS) # GPIO-Pin Setup

while True:
    actual_value = readAnalogData(ADCChannel, SCLK, MOSI, MISO, CS, PAUSE)
    if(abs(actual_value - prev_value) > THRESHOLD):
        print 'Analoger Wert: ', actual_value
    prev_value = actual_value # Aktueller Wert wird alter Wert