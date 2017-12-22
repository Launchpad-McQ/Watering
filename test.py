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

class relay:

    pin = None
    on = False
    def __init__(self, pin = None): #, on = False):
        self.pin = pin
        #self.on = on
        #self.turn(on)

    def turn(self, on):
        if self.on!=on==True:
            self.on = on
            self.loop()
        self.on = on

    def loop(self):
        print("in loop")
        while True:
            if self.on is False:
                consoleprint(str(self.pin) + " Im out")
                break
            consoleprint(str(self.pin) + " im on")
            time.sleep(0.1)

relay1 = relay(0,)
relay1.turn(True)





a=[]
"""
def heron(aoeu):
    global a
    for i in range(0, 5):
        a.append(aoeu)
        time.sleep(aoeu)

#start_new_thread(heron,(0.03,))
#start_new_thread(heron,(0.1,))
threads = []
for i in range(5):
    t = threading.Thread(target=heron, args=(0.1*i,))
    threads.append(t)
    t.start()
time.sleep(1)
print(a)


"""
