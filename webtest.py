import asyncio
import websockets
import json
import relay
import config
import time
import threading
import mcp3008

relaycount = 16
sensorcount = 16
pinlist = [2, 3, 17, 27, 22, 5, 6, 13, 19, 26, 14, 15, 18, 23, 24, 25, 7, 12]

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


def get_reading():
    while True:
        for i in range(0, config.numchip):
            for j in range(0, config.numinputs):
                config.reading_arr[i*config.numinputs+j] = mcp3008.readadc(j, i)
        config.status["sensorval"] = config.reading_arr
        time.sleep(0.5)

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

    start_server = websockets.serve(handler, '192.168.2.144', 9998)
    # start_server = websockets.serve(handler, '192.168.1.210',9998)
    # start_server = websockets.serve(handler, '192.168.2.100',9998)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

except KeyboardInterrupt:
    controller.cleanup()
