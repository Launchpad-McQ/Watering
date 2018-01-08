# from _thread import start_new_thread
import threading
import time
# import mcp3008
import os
import RPi.GPIO as GPIO
# from relaytest import setpins, relayon
import config

pinlist = [2, 3, 4, 17, 27, 22, 5, 6, 13, 19, 26, 14, 15, 18, 23, 24, 25, 7, 12, 16, 20, 21]
relaycount = 16

# For printing to system console. Useful when using multiple threads.
def consoleprint(string):
    os.system("syslog -s -l error \" something " + str(string) + "\"")

# Relay class. Should be started in thread in relayControll.
class Relay:

    pin = None
    on = False

    def __init__(self, pin=None):
        self.pin = pin

    # Turn on relay turn(True) = turn on, turn(False) turn off.
    def turn(self, on, relaynum, duration=3):
        if self.on != on is True:   # Turning relay on.
            GPIO.output(self.pin, GPIO.LOW)
            self.on = on
            config.status["relayon"][relaynum] = self.on
            self.loop(duration, relaynum)
            return
        if self.on != on is False:  # Turning relay off.
            GPIO.output(self.pin, GPIO.HIGH)
            self.on = on
            config.status["relayon"][relaynum] = self.on
            return
    # Loop running untill turned off from other thread.

    def loop(self, duration, relaynum):
        for i in range(1, duration*10):
            if self.on is False:
                GPIO.output(self.pin, GPIO.HIGH)
                config.status["relayon"][relaynum] = self.on
                break
            time.sleep(0.1)
        self.turn(False, relaynum)


class RelayControll:
    global relaycount
    global pinlist
    relays = []
    thread = None

    def __init__(self, pinlist=pinlist, relaycount=relaycount):  # BCM pins. Excluding pins used for SPI0.
        self.relaycount = relaycount
        self.pinlist = pinlist[0: self.relaycount]
        for pin in pinlist:
            self.relays.append(Relay(pin))  # Adding relays to a list.
        self.setpins(pinlist)

    def turnOnRelay(self, relaynum, duration=2):
        self.thread = threading.Thread(target=self.relays[relaynum].turn, args=(True, relaynum, duration))
        self.thread.start()

    def turnOffRelay(self, relaynum, duration=2):
        self.thread = threading.Thread(target=self.relays[relaynum].turn, args=(False, relaynum, duration))
        self.thread.start()
        time.sleep(0.1)

    def setpins(self, pinlist):
        GPIO.setmode(GPIO.BCM)
        # loop through pins and set mode and state to 'low'
        for i in self.pinlist:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)

    # Reset GPIO settings.
    def cleanup(self):
        GPIO.cleanup()

"""
#for test
controll = RelayControll()
controll.turnOnRelay(0,5)
time.sleep(2)
controll.turnOffRelay(0)
controll.turnOnRelay(0,5)
time.sleep(2)
controll.cleanup()
"""
