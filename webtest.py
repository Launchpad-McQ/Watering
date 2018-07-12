import asyncio
import websockets
import json
import relay
import config
import time
import threading
import mcp3008
import time
import RPi.GPIO as GPIO
#from temperature import read_temp

relaycount = 16
sensorcount = 16
# BCM pins.(pin 4 for is for thermometer.)
pinlist = [2, 3, 27, 22, 0, 5, 6, 13, 26, 14, 15, 23, 24, 25, 1, 12]

relayon = [False] * relaycount
sensorval = [0] * sensorcount

# status = {"relayon":relayon, "sensorval":sensorval}

controller = relay.RelayControll(pinlist, relaycount)

# controller.turnOnRelay(relaynum,duration)
"""time.sleep(2)
controller.turnOffRelay(0)
controller.turnOnRelay(0,5)
time.sleep(2)
controller.cleanup()"""
"""
# Getting temperature and storing in config.status[].
temp = read_temp()[0]
config.status["temperature"] = temp
print(config.status["temperature"])
print(config.temperature)
print(time.strftime("%H:%M %d %b %Y, %a "))
"""
# Getting moisture reading and storing in config.status[].
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
def get_reading():
    GPIO.output(16, GPIO.HIGH)
    time.sleep(0.1)
    while True:
        for i in range(0, config.numchip):
            for j in range(0, config.numinputs):
                config.reading_arr[i*config.numinputs+j] = mcp3008.readadc(j, i)
        config.status["sensorval"] = config.reading_arr
        # Sleeping to let the thread finnish getting reading.(?)
        time.sleep(0.5)
    GPIO.output(16, GPIO.LOW)

# Getting reading on new thread(in order to parrallelize).
try:
    thread = threading.Thread(target=get_reading, args=())
    thread.start()

    async def handler(websocket, path):
        consumer_task = asyncio.ensure_future(consumer_handler(websocket))
        producer_task = asyncio.ensure_future(producer_handler(websocket))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

    async def consumer_handler(websocket):
        async for message in websocket:
            await consumer(message)

    async def producer_handler(websocket):
        while True:
            message = await producer()
            await websocket.send(message)
            await asyncio.sleep(0.1)

    async def consumer(message):
        message = json.loads(message)
        relaynum = int(message["relaynum"])
        config.status["duration"] = int(message["duration"])
        if message["turn"] is True:
            controller.turnOnRelay(relaynum, config.status["duration"])

    async def producer():
        message = json.dumps(config.status)
        return message

    start_server = websockets.serve(handler, '192.168.1.202',9998)
    #start_server = websockets.serve(handler, '127.0.0.1', 9998)
    # start_server = websockets.serve(handler, '192.168.2.144', 9998)
    # start_server = websockets.serve(handler, '192.168.1.210',9998)
    # start_server = websockets.serve(handler, '192.168.2.100',9998)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

except KeyboardInterrupt:
    controller.cleanup()
