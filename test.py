#from _thread import start_new_thread
import threading
import time
import mcp3008
import sys
import os
#from relaytest import setpins, relayon

# For printing to system console when using multiple threads.
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
# Relay function. Should be started in thread in relayControll.
class Relay:

    pin = None
    on = False
    def __init__(self, pin = None):
        self.pin = pin

    # Turn on relay#
    def turn(self, on):
        if self.on!=on==True:
            self.on = on
            self.loop()
        self.on = on
        return "hej"
    # Loop running untill turned off from other thread.
    def loop(self):
        print("in loop")
        while True:
            if self.on is False:
                consoleprint(str(self.pin) + " Im out")
                break
            consoleprint(str(self.pin) + " im on")
            time.sleep(0.1)


class RelayControll:

    pinlist = None
    thread = None
    relays = []

    def __init__(self, pinlist = [2, 3, 4, 17, 27, 22, 5, 6, 13, 19, 26, 14, 15, 18, 23, 24, 25, 7, 12, 16, 20, 21], relaycount = 16): #BCM pins. Excluding pins used for SPI0.
        self.pinlist = pinlist[0: relaycount]
        for pin in pinlist:
            self.relays.append(Relay(pin)) #Adding relays to a list.

    def turnOnRelay(self, relaynum):
        self.thread = threading.Thread(target=self.relays[relaynum].turn, args=(True,))
        self.thread.start()

    def turnOffRelay(self, relaynum):
        self.thread = threading.Thread(target=self.relays[relaynum].turn, args=(False,))
        self.thread.start()



controll = RelayControll()
controll.turnOnRelay(0)
time.sleep(2)
print("turinge off")
controll.turnOffRelay(0)


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

