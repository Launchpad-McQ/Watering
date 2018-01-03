# from _thread import start_new_thread
import threading
import time
# import mcp3008
import os
import RPi.GPIO as GPIO
# from relaytest import setpins, relayon


# For printing to system console. Useful when using multiple threads.
def consoleprint(string):
    os.system("syslog -s -l error \" something " + str(string) + "\"")


"""
print(mcp3008.readadc(1))
setpins()
relayon(9,0.3)
time.sleep(0.3)
relayon(9,0.3)
time.sleep(0.3)
relayon(9,0.3)
time.sleep(0.3)
"""


# Relay class. Should be started in thread in relayControll.
class Relay:

    pin = None
    on = False

    def __init__(self, pin=None):
        self.pin = pin

    # Turn on relay#
    def turn(self, on):
        if self.on != on is True:   # Turning relay on.
            GPIO.output(self.pin, GPIO.LOW)
            self.on = on
            return
        if self.on != on is False:  # Turning relay off.
            GPIO.output(self.pin, GPIO.HIGH)
            self.on = on
            return
    # Loop running untill turned off from other thread.

    def loop(self):
        print("in loop")
        while True:
            if self.on is False:
                GPIO.output(self.pin, GPIO.HIGH)
                consoleprint(str(self.pin) + " Im out")
                break
            consoleprint(str(self.pin) + " im on")
            time.sleep(0.1)


class RelayControll:
    pinlist = None
    relays = []
    thread = None

    def __init__(self, pinlist=[2, 3, 4, 17, 27, 22, 5, 6, 13, 19, 26, 14, 15,
                                18, 23, 24, 25, 7, 12, 16, 20, 21],
                 relaycount=16):  # BCM pins. Excluding pins used for SPI0.
        self.pinlist = pinlist[0: relaycount]
        for pin in pinlist:
            self.relays.append(Relay(pin))  # Adding relays to a list.
        self.setpins(pinlist)

    def turnOnRelay(self, relaynum):
        self.relays[relaynum].turn(True)

    def turnOffRelay(self, relaynum):
        self.relays[relaynum].turn(False)

    def setpins(self, pinist):
        GPIO.setmode(GPIO.BCM)
        # loop through pins and set mode and state to 'low'
        for i in self.pinlist:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)

    # Relay on for desired duration (delay).
    def ontimer(self, relaynum, delay):
        self.relays[relaynum].turn(True)
        consoleprint("thread relay on")
        time.sleep(delay)
        self.relays[relaynum].turn(False)
        consoleprint("thread relay off")

    # Turning on relay in new thread.
    def onbutton(self, relaynum, delay):
        self.thread = threading.Thread(target=self.ontimer, args=(relaynum,
                                                                  delay, ))
        self.thread.start()

    # Reset GPIO settings.
    def cleanup(self):
        GPIO.cleanup()

controll = RelayControll()
controll.onbutton(0, 3)
controll.turnOffRelay(0)
time.sleep(1)
controll.turnOnRelay(0)
time.sleep(10)
controll.cleanup()

"""
relay1 = Relay(0,)
relay2 = Relay(0,)
t1 = threading.Thread(target=relay1.turn, args=(True,))
t1.start()
time.sleep(1)
t1 = threading.Thread(target=relay1.turn, args=(False,))
print(threading.activeCount())
t1.start()
print("slutet")

"""
